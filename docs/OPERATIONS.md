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
| Research agents | `OPENAI_API_KEY` |
| Commit proposals | `GEMINI_API_KEY`, `GEMINI_COMMIT_MODELS`, `GROQ_API_KEY`, `GROQ_BASE_URL`, `GROQ_COMMIT_MODEL`, `COMMIT_GENERATION_TIMEOUT` |

The complete list and non-private examples live in `.env.example`.

The research model and number of searches are versioned in `config.py`. Change `MODEL_NAME` or `HOW_MANY_SEARCHES` there so the selected behavior is reviewed and committed with the code.

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

The publishing script verifies the repository, builds a bounded representation of changed paths and text diffs, and requests an English Conventional Commit title and description. The fallback order is the comma-separated `GEMINI_COMMIT_MODELS` list followed by `GROQ_COMMIT_MODEL`. Its defaults match Agentic Twin: Gemini 3.5 Flash, Gemini 3.7 Flash, Gemini 3.5 Flash-Lite, Gemini 3.1 Flash-Lite, then Groq `openai/gpt-oss-120b`.

The command displays the proposal and requires typing `PUBLISH` before staging, re-verifying, committing, and pushing. To avoid external generation, provide both `--title` and `--description`. Cancellation before confirmation leaves the working tree unchanged.

## Diagnostics and recovery

- If startup fails, confirm the environment variables and installed dependencies without printing secrets.
- If research fails, verify the configured model, API quota, and web-search availability.
- If publication metadata generation fails, review each reported provider attempt or supply `--title` and `--description` explicitly.
