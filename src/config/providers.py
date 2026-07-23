import json
from .paths import CONFIG_PATH

config = {}

if CONFIG_PATH.is_file():
    config = json.loads(CONFIG_PATH.read_text())

DEFAULT_MODELS = {
    "OpenAI": "gpt-4o-mini",
    "Ollama": "qwen3:1.7b",
    "Anthropic": "claude-haiku-4-5",
}

# LLM
LLM_PROVIDER = config.get("LLM_PROVIDER") or "OpenAI"
MODEL = config.get("MODEL") or DEFAULT_MODELS.get(LLM_PROVIDER, DEFAULT_MODELS["OpenAI"])

# Web Search
WEB_SEARCH_PROVIDER = config.get("WEB_SEARCH_PROVIDER") or "DuckDuckGo"