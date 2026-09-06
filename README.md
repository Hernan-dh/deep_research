# Deep Research

A bilingual research assistant that plans several web searches, gathers result snippets concurrently, and writes a report with five unique source links.

## Attribution

Project built from [Ed Donner's agentic AI engineering course](https://github.com/ed-donner/agents). The upstream MIT copyright notice is preserved in [LICENSE](LICENSE). No endorsement by the course author is implied.

## Run locally

Python 3.12 and uv are the documented development baseline.  Run the following commands from this repository's root.

```sh
uv venv
uv pip install -r requirements.txt
```

Copy `.env.example` to `.env` (`Copy-Item .env.example .env` in PowerShell, or `cp .env.example .env` on Linux/macOS), then replace only the placeholders for the providers you intend to use. Leave unused credentials empty. Never commit the real `.env`.

Configure at least one model-provider key and `SERPER_API_KEY` for live search. Google Custom Search is optional and requires both Google variables; DDGS is the keyless fallback. Open `http://127.0.0.1:7860` and submit a research question.

```sh
uv run --no-project python app.py
```

## Download results

After a request completes, choose Markdown (.md), Word (.docx) or PDF (.pdf),
then select **Prepare download** and click the generated file. Spanish controls
use **Preparar descarga**. Downloads contain the last completed report in that
chat, including sources. Starting another request clears the previous download.

Markdown preserves the original result. DOCX and PDF retain headings, lists,
tables and source URLs with a simplified layout; they do not reproduce the chat
styling or fetch external images. PDF uses an embedded font for English and
Spanish; glyph coverage for other scripts is limited. Files are temporary, so
save a local copy.

## Architecture

```text
Gradio query -> structured planner -> Serper / Google / DDGS fallback -> writer -> deterministic source selection
```

See [architecture](docs/ARCHITECTURE.md) for components, data flow and trust boundaries, and [operations](docs/OPERATIONS.md) for configuration and recovery.

## Technologies

Python, Gradio, OpenAI Agents SDK, OpenAI Python SDK, Pydantic, requests, DDGS and asyncio. The SDK connects to Gemini, Groq and OpenRouter; the main workflow does not require OpenAI models.

## Reproducible tests

After installing the dependencies above:

```sh
uv run --no-project python -m unittest discover -v
uv run --no-project python scripts/verify.py
```

Coverage: Source deduplication and insufficient-source failure, report construction, structured-output validation and search fallback; network and model calls are mocked. Tests run without real credentials or paid API calls. They do not measure model quality, live provider availability, or full browser behavior. CI installs dependencies and runs the same verifier on pushes and pull requests.

## Limitations

Reports summarize search snippets rather than exhaustively reading or verifying every source. Five genuine URLs do not prove that every claim is supported. Fewer than five unique available sources causes the request to fail. Search services and models can throttle or change; no availability or factual-accuracy guarantee is provided. Legacy email helpers are not part of the main chat workflow.

Prompts and relevant context are sent to external model/search providers. Do not submit secrets or confidential data. Provider names in source code are configuration, not promises of current availability, pricing, or free access.

## Public repository and license

The repository includes a placeholder-only [.env.example](.env.example); local credentials, caches and generated artifacts are excluded by [.gitignore](.gitignore). See [operations](docs/OPERATIONS.md) for verification and publication instructions.

The code is distributed under the [MIT license](LICENSE). Dependencies retain their own licenses. Biographical material, third-party documents, logos and linked content are not relicensed by this code license. Publishing scripts can send code diffs to external models when generating commit text; use explicit metadata to avoid that step.
