import os
from dotenv import load_dotenv
from config import PROVIDER, BASE_URL, MODEL, MAX_TOKENS
from .anthropic import AnthropicLLM

load_dotenv()

# Choose the provider's class based on the provider and other configurations set in src/config/provider.py
if PROVIDER == "Anthropic":
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set. Set it in .env before running Mosfet.")
    
    llm = AnthropicLLM(api_key, MODEL, MAX_TOKENS)
else:
    raise RuntimeError(f"No adapter implemented yet for PROVIDER '{PROVIDER}'.")