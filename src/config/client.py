import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from .provider import PROVIDER, BASE_URL, MODEL, MAX_TOKENS

load_dotenv()

# Make sure that the provider is set.
if not PROVIDER:
    raise RuntimeError("PROVIDER is not selected. Select it from src/config/provider.py before running Mosfet.")

# Make sure all the required keys for the provider are provided.
if PROVIDER == "OpenAI":
    base_url = None
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Add it to your .env file before running Mosfet.")
    
    client = OpenAI(api_key=api_key, base_url=base_url)
elif PROVIDER == "Ollama":
    base_url = BASE_URL
    # Local server ignores the key, but the SDK requires a non-empty string
    api_key = "ollama"

    if not base_url:
        raise RuntimeError("BASE_URL is not set for Ollama. Set it in src/config/provider.py before running Mosfet.")
    
    client = OpenAI(api_key=api_key, base_url=base_url)
elif PROVIDER == "Anthropic":
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set. Set it in src/config/provider.py before running Mosfet.")
    
    client = Anthropic(api_key=api_key)

    max_tokens = MAX_TOKENS
else:
    raise RuntimeError(f"Unknown PROVIDER '{PROVIDER}'. Use from the list of providers in src/config/provider.py.")


model = MODEL