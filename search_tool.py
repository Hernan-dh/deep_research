"""Web search with Serper, Google Custom Search, and a keyless DDGS fallback."""

from __future__ import annotations

import os
import time

from ddgs import DDGS
from ddgs.exceptions import DDGSException
import requests

from config import (
    GOOGLE_SEARCH_API_URL,
    SEARCH_PROVIDER_ORDER,
    SEARCH_REQUEST_TIMEOUT_SECONDS,
    SEARCH_RESULTS_PER_QUERY,
    SEARCH_RETRIES,
    SEARCH_RETRY_DELAY_SECONDS,
    SERPER_SEARCH_API_URL,
)


def _search_serper(query: str) -> list[dict[str, str]]:
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise RuntimeError("Serper credentials are not configured.")
    response = requests.post(
        SERPER_SEARCH_API_URL,
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
        json={"q": query, "num": min(SEARCH_RESULTS_PER_QUERY, 10)},
        timeout=SEARCH_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    results = [
        {"title": item.get("title", ""), "url": item.get("link", ""),
         "snippet": item.get("snippet", "")[:500]}
        for item in response.json().get("organic", [])
        if item.get("link")
    ]
    if not results:
        raise RuntimeError("Serper returned no usable URLs.")
    return results


def _search_google(query: str) -> list[dict[str, str]]:
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    if not api_key or not engine_id:
        raise RuntimeError("Google Custom Search credentials are not configured.")

    response = requests.get(
        GOOGLE_SEARCH_API_URL,
        params={
            "key": api_key,
            "cx": engine_id,
            "q": query,
            "num": min(SEARCH_RESULTS_PER_QUERY, 10),
        },
        timeout=SEARCH_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    results = [
        {
            "title": item.get("title", ""),
            "url": item.get("link", ""),
            "snippet": item.get("snippet", "")[:500],
        }
        for item in response.json().get("items", [])
        if item.get("link")
    ]
    if not results:
        raise RuntimeError("Google Custom Search returned no usable URLs.")
    return results


def _search_ddgs(query: str) -> list[dict[str, str]]:
    last_error: Exception | None = None
    for attempt in range(SEARCH_RETRIES + 1):
        try:
            results = DDGS(timeout=SEARCH_REQUEST_TIMEOUT_SECONDS).text(
                query,
                max_results=SEARCH_RESULTS_PER_QUERY,
            )
            normalized = [
                {
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")[:500],
                }
                for result in results
                if result.get("href")
            ]
            if normalized:
                return normalized
            raise DDGSException("Search returned no usable URLs.")
        except DDGSException as error:
            last_error = error
            if attempt < SEARCH_RETRIES:
                time.sleep(SEARCH_RETRY_DELAY_SECONDS * (attempt + 1))
    raise RuntimeError(f"DDGS failed after {SEARCH_RETRIES + 1} attempts.") from last_error


def search_web(query: str) -> list[dict[str, str]]:
    """Try configured search providers in order without exposing credentials."""
    errors: list[str] = []
    for provider in SEARCH_PROVIDER_ORDER:
        try:
            if provider == "serper":
                return _search_serper(query)
            if provider == "google":
                return _search_google(query)
            if provider == "ddgs":
                return _search_ddgs(query)
            errors.append(f"{provider}: unsupported provider")
        except (RuntimeError, requests.RequestException, ValueError, DDGSException) as error:
            errors.append(f"{provider}: {type(error).__name__}")
    attempted = ", ".join(SEARCH_PROVIDER_ORDER)
    details = "; ".join(errors)
    raise RuntimeError(f"All search providers failed ({attempted}). {details}")
