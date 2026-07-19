LLM_PROVIDER="OpenAI" # OpenAI, Ollama, Anthropic
# Defaults to DDG if not customized or set because it does not need any API. This ensures that the agent still has web search capability regardless.
WEB_SEARCH_PROVIDER="Brave" # DuckDuckGo, Brave

"""
Ollama: qwen3:1.7b
OpenAI: gpt-4o-mini
Anthropic: claude-opus-4-8
"""
MODEL="gpt-4o-mini"

# Ollama
BASE_URL="http://localhost:11434/v1"

# Anthropic
MAX_TOKENS=4096

# DuckDuckGo
MAX_RESULTS = 5