import json
from .paths import CONFIG_PATH

config = {}

if CONFIG_PATH.is_file():
    config = json.loads(CONFIG_PATH.read_text())

# LLM
LLM_PROVIDER = config.get("LLM_PROVIDER") or "OpenAI"
MODEL = config.get("MODEL") or "gpt-4o-mini"

# Web Search
WEB_SEARCH_PROVIDER = config.get("WEB_SEARCH_PROVIDER") or "DuckDuckGo"