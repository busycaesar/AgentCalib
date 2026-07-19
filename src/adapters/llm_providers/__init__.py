import os
from dotenv import load_dotenv
from config import LLM_PROVIDER, BASE_URL, MODEL, MAX_TOKENS
from .anthropic import AnthropicLLM
from .ollama import OllamaLLM
from .openai import OpenAILLM

load_dotenv()

# Choose the provider's class based on the provider and other configurations set in src/config/provider.py
if LLM_PROVIDER == "Anthropic":
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set. Set it in .env before running Mosfet.")
    
    llm = AnthropicLLM(api_key, MODEL, MAX_TOKENS)
elif LLM_PROVIDER == "Ollama":
    if not BASE_URL:
        raise RuntimeError("BASE_URL is not set for Ollama. Set it in /src/config/provider before running Mosfet.")
    
    llm = OllamaLLM(BASE_URL, MODEL)
elif LLM_PROVIDER == "OpenAI":
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Set it in .env before running Mosfet.")
    
    llm = OpenAILLM(api_key, MODEL)
else:
    raise RuntimeError(f"No adapter implemented yet for LLM_PROVIDER '{LLM_PROVIDER}'.")