# Operations

## Local execution

1. Create and activate a virtual environment.
2. Run `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and set local values.
4. Run `python app.py`.

`.env` is excluded from Git and must never be copied into documentation, commits, or diagnostic output.

## Configuration

| Group | Variables |
|---|---|
| Research agents | `GROQ_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY` |
| Web search | `GOOGLE_SEARCH_API_KEY`, `GOOGLE_SEARCH_ENGINE_ID` |
| Commit proposals | `GEMINI_API_KEY`, `GEMINI_COMMIT_MODELS`, `GROQ_API_KEY`, `GROQ_BASE_URL`, `GROQ_COMMIT_MODEL`, `COMMIT_GENERATION_TIMEOUT` |

The complete list and non-private examples live in `.env.example`.

The Gemini models, Groq fallback, provider endpoints, model timeout, search count, search provider order, search concurrency, search timeout, retries, and results per query are versioned in `config.py`. These settings are reviewed and committed with the code. Four bounded results per query keep the final writer prompt within practical provider quotas.

## Model fallback

Normal requests use Gemini 3.8 Flash. Recoverable provider or model-output failures try Gemini 3.7/3.6 Flash, Groq GPT-OSS 120B, and OpenRouter Nemotron 3 Ultra/Super Free. Each API request has a 90-second timeout; retries are controlled by this explicit chain rather than hidden client retries. Programming errors are not swallowed by the fallback chain. Provider keys are configured through the environment; model names and endpoints remain versioned. OpenAI tracing is disabled. Search tries Google Custom Search first, using its API key and Programmable Search Engine ID, then DDGS. DDGS requires no key, so research remains available when Google is not configured, has exhausted its quota, times out, or returns no usable results.

## Render deployment

The repository includes `render.yaml` for a free Render web service. It installs `requirements.txt`, starts with `python app.py`, and prompts for the four secret provider variables during Blueprint creation. The application binds to `0.0.0.0` and Render's `PORT`; locally it defaults to port 7860.

After deployment, test one research request in each language and confirm that the final report includes five working source links. Free services may suspend while inactive, so the first request after inactivity can be slower.

## Verification

```bash
./scripts/verify.sh
```

The command checks Python syntax, existing tests, diffs, potential secrets, private or generated files, file sizes, and essential documentation.

Enable the local pre-commit check once per clone:

```bash
python scripts/install_hooks.py
```

GitHub Actions invokes the same `scripts/verify.sh` implementation.

## Publishing

Safe preview without staging or publishing:

```bash
python scripts/publish.py --preview
```

Interactive publication:

```bash
python scripts/publish.py
```

The publishing script verifies the repository, builds a bounded representation of changed paths and text diffs, and requests an English Conventional Commit title and description. The fallback order is the comma-separated `GEMINI_COMMIT_MODELS` list followed by `GROQ_COMMIT_MODEL`. Its quality-first defaults match Agentic Twin: Gemini 3.8 Flash, Gemini 3.7 Flash, Gemini 3.6 Flash, Gemini 3.5 Flash, Gemini 3.5 Flash-Lite, Gemini 3.1 Flash-Lite, then Groq `openai/gpt-oss-120b`.

The command displays the proposal and requires typing `PUBLISH` before staging, re-verifying, committing, and pushing. To avoid external generation, provide both `--title` and `--description`. Cancellation before confirmation leaves the working tree unchanged.

## Diagnostics and recovery

- If startup fails, confirm the environment variables and installed dependencies without printing secrets.
- Logs identify every attempted model and the model that completed the request.
- If Gemini models fail, confirm `GEMINI_API_KEY`, model availability, and provider quota.
- If the cross-provider fallback fails, confirm the Gemini, Groq, and OpenRouter keys, configured model names, and provider quotas.
- If the planner returns malformed JSON, local Pydantic validation advances to the next model. The writer returns Markdown and source links are selected directly from search data, avoiding provider-side schema enforcement.
- If Google search is skipped or fails, confirm `GOOGLE_SEARCH_API_KEY`, `GOOGLE_SEARCH_ENGINE_ID`, API enablement, quota, and Programmable Search Engine configuration. The application then falls back automatically to DDGS.
- If every search provider fails, verify outbound internet access and DDGS backend availability. Searches run with concurrency two and a ten-second timeout; DDGS uses two bounded retries.
- If a report cannot be completed, inspect its trace to confirm that searches returned at least five usable source URLs.
- If publication metadata generation fails, review each reported provider attempt or supply `--title` and `--description` explicitly.
