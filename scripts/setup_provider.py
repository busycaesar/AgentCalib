"""
Interactive setup for mosfet.config.json and .env, run by install.sh.
Uses arrow-key single-select prompts (same interaction pattern as Claude Code's
own setup prompts) instead of a numbered menu.
"""

import json
from pathlib import Path

import questionary

INSTALL_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = INSTALL_DIR / "mosfet.config.json"
CONFIG_EXAMPLE = INSTALL_DIR / "mosfet.config.example.json"
ENV_FILE = INSTALL_DIR / ".env"
ENV_EXAMPLE = INSTALL_DIR / ".env.example"

SKIP = "Skip (use the default)"

LLM_API_KEY_ENV = {
    "OpenAI": "OPENAI_API_KEY",
    "Anthropic": "ANTHROPIC_API_KEY",
}


def prompt_secret(env_key):
    api_key = questionary.password(f"{env_key}:").ask()

    if not api_key:
        print(f"Warning: no API key entered. Edit .env before running mosfet.")
        return None

    return api_key


def setup_config():
    if CONFIG_FILE.is_file():
        print("mosfet.config.json already exists, skipping provider setup.")
        return {}

    config = json.loads(CONFIG_EXAMPLE.read_text())
    secrets = {}

    llm_provider = questionary.select(
        "Which LLM provider would you like to use?",
        choices=["OpenAI", "Ollama", "Anthropic", SKIP],
    ).ask()

    if llm_provider and llm_provider != SKIP:
        config["LLM_PROVIDER"] = llm_provider

        model = questionary.text("Model to use (leave blank to use the default):").ask()
        config["MODEL"] = (model or "").strip()

        env_key = LLM_API_KEY_ENV.get(llm_provider)
        if env_key:
            api_key = prompt_secret(env_key)
            if api_key:
                secrets[env_key] = api_key

    web_search_provider = questionary.select(
        "Which web search provider would you like to use?",
        choices=["DuckDuckGo", "Brave", SKIP],
    ).ask()

    if web_search_provider and web_search_provider != SKIP:
        config["WEB_SEARCH_PROVIDER"] = web_search_provider

        if web_search_provider == "Brave":
            api_key = prompt_secret("BRAVE_API_KEY")
            if api_key:
                secrets["BRAVE_API_KEY"] = api_key

    CONFIG_FILE.write_text(json.dumps(config, indent=2) + "\n")

    return secrets


def setup_env(secrets):
    if ENV_FILE.is_file():
        print(".env already exists, skipping credential prompt.")
        return

    env_content = ENV_EXAMPLE.read_text()

    for key, value in secrets.items():
        env_content = env_content.replace(f'{key}=""', f'{key}="{value}"')

    ENV_FILE.write_text(env_content)
    ENV_FILE.chmod(0o600)  # restrict permissions since the file holds secrets


if __name__ == "__main__":
    collected_secrets = setup_config()
    setup_env(collected_secrets)
