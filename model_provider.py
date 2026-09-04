"""Quality-first Gemini model configuration with a cross-provider fallback."""

from __future__ import annotations

import json
import os
import re
from typing import TypeVar

from agents import Agent, OpenAIChatCompletionsModel, RunConfig, Runner, set_tracing_disabled
from agents.exceptions import ModelBehaviorError
from dotenv import load_dotenv
from openai import APIError, AsyncOpenAI
from pydantic import BaseModel, ValidationError

from config import (
    FALLBACK_MODEL_BASE_URL,
    FALLBACK_MODEL_NAME,
    MODEL_REQUEST_TIMEOUT_SECONDS,
    OPENROUTER_MODEL_BASE_URL,
    OPENROUTER_MODEL_NAMES,
    PRIMARY_MODEL_BASE_URL,
    PRIMARY_MODEL_NAME,
    SECONDARY_MODEL_BASE_URL,
    SECONDARY_MODEL_NAME,
    TERTIARY_MODEL_BASE_URL,
    TERTIARY_MODEL_NAME,
)

load_dotenv(override=True)
set_tracing_disabled(True)

_groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
_gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
_openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
GROQ_CLIENT_PLACEHOLDER = "not-configured"
GEMINI_CLIENT_PLACEHOLDER = "not-configured"
OPENROUTER_CLIENT_PLACEHOLDER = "not-configured"

PRIMARY_MODEL = OpenAIChatCompletionsModel(
    model=PRIMARY_MODEL_NAME,
    openai_client=AsyncOpenAI(
        api_key=_gemini_api_key or GEMINI_CLIENT_PLACEHOLDER,
        base_url=PRIMARY_MODEL_BASE_URL,
        timeout=MODEL_REQUEST_TIMEOUT_SECONDS,
        max_retries=0,
    ),
)

SECONDARY_MODEL = OpenAIChatCompletionsModel(
    model=SECONDARY_MODEL_NAME,
    openai_client=AsyncOpenAI(
        api_key=_gemini_api_key or GEMINI_CLIENT_PLACEHOLDER,
        base_url=SECONDARY_MODEL_BASE_URL,
        timeout=MODEL_REQUEST_TIMEOUT_SECONDS,
        max_retries=0,
    ),
)

TERTIARY_MODEL = OpenAIChatCompletionsModel(
    model=TERTIARY_MODEL_NAME,
    openai_client=AsyncOpenAI(
        api_key=_gemini_api_key or GEMINI_CLIENT_PLACEHOLDER,
        base_url=TERTIARY_MODEL_BASE_URL,
        timeout=MODEL_REQUEST_TIMEOUT_SECONDS,
        max_retries=0,
    ),
)

FALLBACK_MODEL = OpenAIChatCompletionsModel(
    model=FALLBACK_MODEL_NAME,
    openai_client=AsyncOpenAI(
        api_key=_groq_api_key or GROQ_CLIENT_PLACEHOLDER,
        base_url=FALLBACK_MODEL_BASE_URL,
        timeout=MODEL_REQUEST_TIMEOUT_SECONDS,
        max_retries=0,
    ),
)

OPENROUTER_MODELS = tuple(
    OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=AsyncOpenAI(
            api_key=_openrouter_api_key or OPENROUTER_CLIENT_PLACEHOLDER,
            base_url=OPENROUTER_MODEL_BASE_URL,
            timeout=MODEL_REQUEST_TIMEOUT_SECONDS,
            max_retries=0,
        ),
    )
    for model_name in OPENROUTER_MODEL_NAMES
)

RECOVERABLE_MODEL_ERRORS = (APIError, ModelBehaviorError, ValidationError)
StructuredOutput = TypeVar("StructuredOutput", bound=BaseModel)


class StructuredOutputError(ValueError):
    """A provider returned text that cannot satisfy the local schema."""


def parse_structured_output(text: object, output_type: type[StructuredOutput]) -> StructuredOutput:
    """Extract a JSON object from model text and validate it locally."""
    if isinstance(text, output_type):
        return text
    if not isinstance(text, str):
        raise StructuredOutputError("The model returned no text output.")
    candidate = text.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", candidate, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        candidate = fenced.group(1).strip()
    start = candidate.find("{")
    end = candidate.rfind("}")
    if start < 0 or end < start:
        raise StructuredOutputError("The model returned no JSON object.")
    try:
        payload = json.loads(candidate[start : end + 1])
        return output_type.model_validate(payload)
    except (json.JSONDecodeError, ValidationError, TypeError) as error:
        raise StructuredOutputError("The model returned invalid structured output.") from error


async def run_with_fallback(
    agent: Agent,
    input_message: str,
    output_type: type[StructuredOutput] | None = None,
):
    """Try quality-ordered models and preserve programming errors."""
    attempts: list[tuple[str, OpenAIChatCompletionsModel]] = []
    if _gemini_api_key:
        attempts.extend(
            (
                (f"Gemini/{PRIMARY_MODEL_NAME}", PRIMARY_MODEL),
                (f"Gemini/{SECONDARY_MODEL_NAME}", SECONDARY_MODEL),
                (f"Gemini/{TERTIARY_MODEL_NAME}", TERTIARY_MODEL),
            )
        )
    else:
        print("[models] GEMINI_API_KEY is not configured; skipping Gemini models")
    if _groq_api_key:
        attempts.append((f"Groq/{FALLBACK_MODEL_NAME}", FALLBACK_MODEL))
    else:
        print("[models] GROQ_API_KEY is not configured; skipping Groq")
    if _openrouter_api_key:
        attempts.extend(
            (f"OpenRouter/{name}", model)
            for name, model in zip(OPENROUTER_MODEL_NAMES, OPENROUTER_MODELS)
        )
    else:
        print("[models] OPENROUTER_API_KEY is not configured; skipping OpenRouter")

    if not attempts:
        raise RuntimeError(
            "Configure GEMINI_API_KEY, GROQ_API_KEY, or OPENROUTER_API_KEY "
            "to run the research agents."
        )

    failures: list[str] = []
    for label, model in attempts:
        print(f"[models] trying {label}")
        try:
            result = await Runner.run(
                agent,
                input_message,
                run_config=RunConfig(model=model, tracing_disabled=True),
            )
            final_output = (
                parse_structured_output(result.final_output, output_type)
                if output_type is not None
                else result.final_output
            )
            print(f"[models] completed with {label}")
            return final_output
        except (*RECOVERABLE_MODEL_ERRORS, StructuredOutputError) as error:
            failures.append(f"{label}: {type(error).__name__}")
            print(f"[models] {label} failed ({type(error).__name__}); trying next model")

    raise RuntimeError("All configured models failed: " + "; ".join(failures))
