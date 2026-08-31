"""Version-controlled application settings."""

PRIMARY_MODEL_NAME = "gemini-3.7-flash"
PRIMARY_MODEL_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
SECONDARY_MODEL_NAME = "gemini-3.6-flash"
SECONDARY_MODEL_BASE_URL = PRIMARY_MODEL_BASE_URL
FALLBACK_MODEL_NAME = "openai/gpt-oss-120b"
FALLBACK_MODEL_BASE_URL = "https://api.groq.com/openai/v1"
MODEL_REQUEST_TIMEOUT_SECONDS = 90
MODEL_NAME = PRIMARY_MODEL_NAME
HOW_MANY_SEARCHES = 5
SEARCH_RESULTS_PER_QUERY = 4
SEARCH_CONCURRENCY = 2
SEARCH_REQUEST_TIMEOUT_SECONDS = 10
SEARCH_RETRIES = 2
SEARCH_RETRY_DELAY_SECONDS = 1
SEARCH_PROVIDER_ORDER = ("google", "ddgs")
GOOGLE_SEARCH_API_URL = "https://customsearch.googleapis.com/customsearch/v1"
