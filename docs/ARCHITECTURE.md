# Architecture

## Purpose

Deep Research is a Gradio application that plans web searches, runs them concurrently, synthesizes a structured report, and sends the result by email or push notification.

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
  |-- Search Agents + WebSearchTool
  |-- Writer Agent
  `-- Email Agent --> SMTP or Pushover
```

- `app.py`: Gradio interface and streaming status updates.
- `research_manager.py`: orchestration, tracing, concurrency, and handoff between stages.
- `planner_agent.py`: produces a structured search plan.
- `search_agent.py`: executes web searches and summarizes results.
- `writer_agent.py`: produces the structured final report.
- `email_agent.py` and `messenger.py`: deliver the report through configured notification services.
- `scripts/publish.py`: verifies changes and requests commit metadata through a Gemini-to-Groq fallback before a human-confirmed Git publication flow.

## Main flow

1. The user submits a research question.
2. The planner creates a configured number of search queries.
3. Search agents execute those queries concurrently.
4. The writer synthesizes the results into a Markdown report.
5. The email agent sends the report, using Pushover when email is disabled.
6. The report is displayed in the web interface.

## Trust boundaries

- User queries, search results, and model responses are untrusted data.
- Credentials come from the environment and must never appear in Git, documentation, prompts, or logs.
- OpenAI, web search, SMTP, and Pushover are external services.
- The publishing script sends Gemini or Groq a size-limited representation of changed paths and text diffs. Provider keys remain in the environment.

## Related decisions

- [Continuous documentation and safe publishing](decisions/0001-continuous-documentation-and-safe-publishing.md)
