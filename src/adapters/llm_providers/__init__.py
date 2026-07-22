from config import LLM_PROVIDER, OLLAMA_BASE_URL, MODEL, ANTHROPIC_MAX_TOKENS, ANTHROPIC_API_KEY, OPENAI_API_KEY
from .anthropic import AnthropicLLM
from .ollama import OllamaLLM
from .openai import OpenAILLM

# Choose the provider's class based on the provider and other configurations set in src/config/provider.py
if LLM_PROVIDER == "Anthropic":
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY is not set. Set it in .env before running Mosfet.")

    llm = AnthropicLLM(ANTHROPIC_API_KEY, MODEL, ANTHROPIC_MAX_TOKENS)
elif LLM_PROVIDER == "Ollama":
    if not OLLAMA_BASE_URL:
        raise RuntimeError("OLLAMA_BASE_URL is not set for Ollama. Set it in /src/config/provider before running Mosfet.")

    llm = OllamaLLM(OLLAMA_BASE_URL, MODEL)
elif LLM_PROVIDER == "OpenAI":
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set. Set it in .env before running Mosfet.")

    llm = OpenAILLM(OPENAI_API_KEY, MODEL)
else:
    raise RuntimeError(f"No adapter implemented yet for LLM_PROVIDER '{LLM_PROVIDER}'.")