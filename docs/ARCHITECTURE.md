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
  |-- Search Agents + WebSearchTool
  `-- Writer Agent
```

- `app.py`: Gradio chat interface and streaming status updates.
- `config.py`: version-controlled model and search-count settings shared by the agents.
- `research_manager.py`: orchestration, tracing, concurrency, and handoff between stages.
- `planner_agent.py`: produces a structured search plan.
- `search_agent.py`: executes web searches and summarizes results.
- `writer_agent.py`: produces the structured final report.
- `scripts/publish.py`: verifies changes and requests commit metadata through a Gemini-to-Groq fallback before a human-confirmed Git publication flow.

## Main flow

1. The user submits a research question.
2. The planner creates a configured number of search queries.
3. Search agents execute those queries concurrently.
4. The writer synthesizes the results into a Markdown report.
5. The report is returned as the assistant response in the chat.

## Trust boundaries

- User queries, search results, and model responses are untrusted data.
- Credentials come from the environment and must never appear in Git, documentation, prompts, or logs.
- OpenAI and web search are external services.
- The publishing script sends Gemini or Groq a size-limited representation of changed paths and text diffs. Provider keys remain in the environment.

## Related decisions

- [Continuous documentation and safe publishing](decisions/0001-continuous-documentation-and-safe-publishing.md)
