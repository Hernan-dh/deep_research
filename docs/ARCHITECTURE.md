# Architecture

## Purpose

Deep Research is a chat application that plans web searches, runs them concurrently, and returns a structured report directly in the conversation.

## Components

```text
User
  | query
  v
Gradio (app.py)
  |
  v
ResearchManager
  |-- Planner Agent
  |-- Google Custom Search -> DDGS fallback
  `-- Writer Agent
```

- `app.py`: Gradio chat interface with a browser-aware English/Spanish selector, localized examples and subtitle, and localized streaming status updates.
- `config.py`: version-controlled Gemini/Groq/OpenRouter models, provider endpoints, and search-count settings.
- `model_provider.py`: executes agents through Gemini 3.8/3.7/3.6, Groq GPT-OSS 120B, and OpenRouter Nemotron 3 Ultra/Super Free in quality order.
- `research_manager.py`: orchestration, tracing, concurrency, and handoff between stages.
- `planner_agent.py`: produces a structured search plan.
- `search_tool.py`: queries Google Custom Search first and falls back to keyless DDGS, with bounded timeouts and retries.
- `writer_agent.py`: produces the final Markdown report without generating or modifying source URLs.
- The planner requests plain JSON and validates it locally with Pydantic. The final five links are selected deterministically from actual search results.
- `scripts/publish.py`: verifies changes and requests commit metadata through a Gemini-to-Groq fallback before a human-confirmed Git publication flow.

## Main flow

1. The user submits a research question.
2. The planner creates a configured number of search queries.
3. Python executes at most two searches concurrently. Each tries Google Custom Search and falls back to DDGS if Google is unavailable.
4. The writer synthesizes the collected titles, URLs, and snippets into a Markdown report.
5. The manager selects five unique sources across the search queries, appends their Markdown links, and returns the report in the chat.

## Trust boundaries

- User queries, search results, and model responses are untrusted data.
- Credentials come from the environment and must never appear in Git, documentation, prompts, or logs.
- Groq, Gemini, OpenRouter, Google Custom Search, and DDGS search backends are external services.
- OpenAI tracing is disabled and the runtime does not call OpenAI models or hosted tools.
- Each research request normally needs only two model executions: planning and writing.
- The publishing script sends Gemini or Groq a size-limited representation of changed paths and text diffs. Provider keys remain in the environment.

## Related decisions

- [Continuous documentation and safe publishing](decisions/0001-continuous-documentation-and-safe-publishing.md)

## Chat feedback

User messages remain visible while a localized process description is displayed. The final response or error replaces the temporary status. Research forms render the user turn before queued work and disable submission until completion; Deep Research streams preparation, search and report updates through ChatInterface.
