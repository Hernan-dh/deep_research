"""Optional Phoenix tracing for OpenAI Agents SDK workflows."""

import logging
import os


logger = logging.getLogger(__name__)


def configure_observability() -> None:
    endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT")
    if not endpoint:
        return
    try:
        from phoenix.otel import register
        from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor

        tracer_provider = register(project_name="deep-research", endpoint=endpoint)
        OpenAIAgentsInstrumentor().instrument(tracer_provider=tracer_provider)
    except Exception:
        logger.warning("Phoenix tracing is unavailable; continuing without it.", exc_info=True)
