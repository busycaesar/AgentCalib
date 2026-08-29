"""
Interactive setup/update for mosfet.config.json and .env, run via `mosfet config`.
Uses arrow-key single-select prompts (same interaction pattern as Claude Code's
own setup prompts) instead of a numbered menu.
"""

import json
import sys

import questionary
from questionary import Choice
from dotenv import dotenv_values

from config import CONFIG_PATH, ENV_PATH, DEFAULT_LLM_PROVIDER, DEFAULT_WEB_SEARCH_PROVIDER, DEFAULT_MODELS

SKIP = "__skip__"
DONE = "Done"

CONFIG_TEMPLATE = {
    "LLM_PROVIDER": "",
    "MODEL": "",
    "WEB_SEARCH_PROVIDER": "",
    "COMMUNICATION_CHANNELS": [],
}

LLM_PROVIDERS = ["OpenAI", "Ollama", "Anthropic"]
WEB_SEARCH_PROVIDER_CHOICES = {
    "DuckDuckGo (Free)": "DuckDuckGo",
    "Brave": "Brave",
}

LLM_API_KEY_ENV = {
    "OpenAI": "OPENAI_API_KEY",
    "Anthropic": "ANTHROPIC_API_KEY",
}
WEB_SEARCH_API_KEY_ENV = {
    "Brave": "BRAVE_API_KEY",
}

# CLI needs no credential and is always available, so it isn't a selectable
# channel here — this only lists channels that need setup.
CHANNEL_API_KEY_ENV = {
    "Discord": "DISCORD_BOT_TOKEN",
}

_pending_warnings = []


def write_env_key(env_key, value):
    """Update (or append) a single KEY="value" line in .env with a plain
    in-place write — not dotenv's set_key(), which writes via a temp file
    + atomic rename. That rename fails with EBUSY when .env is a Docker
    bind-mounted file, since you can't replace the inode a bind mount points
    at."""
    lines = ENV_PATH.read_text().splitlines() if ENV_PATH.is_file() else []
    new_line = f'{env_key}="{value}"'

    for i, line in enumerate(lines):
        if line.startswith(f"{env_key}="):
            lines[i] = new_line
            break
    else:
        lines.append(new_line)

    ENV_PATH.write_text("\n".join(lines) + "\n")


def prompt_credential(env_key):
    """Prompt for a single .env credential, but only if it isn't already set —
    an existing value is left untouched with no prompt. Blank input queues a
    warning that the app won't work until it's filled in — printed together
    with any others at the end of the run."""
    if not ENV_PATH.is_file():
        ENV_PATH.touch(mode=0o600)

    if dotenv_values(ENV_PATH).get(env_key):
        return

    value = questionary.password(f"{env_key}:").ask()

    if not value:
        _pending_warnings.append(f"{env_key} is not set. The app won't work until you set it in {ENV_PATH}.")
        return

    write_env_key(env_key, value)


def print_pending_warnings():
    for warning in _pending_warnings:
        print(f"Warning: {warning}")
    _pending_warnings.clear()


def prompt_channels(config):
    """Multi-select which non-CLI channels to set up. Selection is stored in
    config (COMMUNICATION_CHANNELS) independent of whether a credential was
    actually filled in, so a channel picked but left blank still shows as
    selected next time instead of looking untouched."""
    current = config.get("COMMUNICATION_CHANNELS") or []

    selected_channels = questionary.checkbox(
        "Which communication channels would you like to set up? (CLI is always available)",
        choices=[
            *[Choice(title=channel, value=channel, checked=channel in current) 
            for channel in CHANNEL_API_KEY_ENV],
            Choice(title="Skip", value=SKIP),
        ],
    ).ask()

    if not selected_channels or SKIP in selected_channels:
        selected_channels = []

    config["COMMUNICATION_CHANNELS"] = selected_channels

    for channel in selected_channels:
        prompt_credential(CHANNEL_API_KEY_ENV[channel])


def setup_config():
    config = dict(CONFIG_TEMPLATE)

    llm_provider = questionary.select(
        "Which LLM provider would you like to use?",
        choices=[*LLM_PROVIDERS, Choice(title=f"Skip (use the default: {DEFAULT_LLM_PROVIDER})", value=SKIP)],
    ).ask()

    if llm_provider and llm_provider != SKIP:
        config["LLM_PROVIDER"] = llm_provider

        default_model = DEFAULT_MODELS.get(llm_provider, DEFAULT_MODELS[DEFAULT_LLM_PROVIDER])
        model = questionary.text(f"Model to use (leave blank to use the default: {default_model}):").ask()
        config["MODEL"] = (model or "").strip()

        env_key = LLM_API_KEY_ENV.get(llm_provider)
        if env_key:
            prompt_credential(env_key)

    web_search_provider = questionary.select(
        "Which web search provider would you like to use?",
        choices=[
            *[Choice(title=title, value=value) for title, value in WEB_SEARCH_PROVIDER_CHOICES.items()],
            Choice(title=f"Skip (use the default: {DEFAULT_WEB_SEARCH_PROVIDER})", value=SKIP),
        ],
    ).ask()

    if web_search_provider and web_search_provider != SKIP:
        config["WEB_SEARCH_PROVIDER"] = web_search_provider

        env_key = WEB_SEARCH_API_KEY_ENV.get(web_search_provider)
        if env_key:
            prompt_credential(env_key)

    prompt_channels(config)

    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")
    print(f"Wrote {CONFIG_PATH}.")
    print_pending_warnings()


def update_config():
    config = json.loads(CONFIG_PATH.read_text())

    while True:
        channels = config.get("COMMUNICATION_CHANNELS") or []

        print()
        print(f"LLM_PROVIDER: {config.get('LLM_PROVIDER') or '(default)'}")
        print(f"MODEL: {config.get('MODEL') or '(default)'}")
        print(f"WEB_SEARCH_PROVIDER: {config.get('WEB_SEARCH_PROVIDER') or '(default)'}")
        print(f"Communication Channels: CLI, {', '.join(channels)}" if channels else "Communication Channels: CLI")

        choice = questionary.select(
            "What would you like to update?",
            choices=["LLM Provider", "Model", "Web Search Provider", "Communication Channels", DONE],
        ).ask()

        if not choice or choice == DONE:
            break

        if choice == "LLM Provider":
            llm_provider = questionary.select(
                "Which LLM provider would you like to use?",
                choices=LLM_PROVIDERS,
                default=config.get("LLM_PROVIDER") if config.get("LLM_PROVIDER") in LLM_PROVIDERS else None,
            ).ask()

            if llm_provider and llm_provider != config.get("LLM_PROVIDER"):
                config["LLM_PROVIDER"] = llm_provider

                env_key = LLM_API_KEY_ENV.get(llm_provider)
                if env_key:
                    prompt_credential(env_key)

        elif choice == "Model":
            current_provider = config.get("LLM_PROVIDER") or DEFAULT_LLM_PROVIDER
            default_model = DEFAULT_MODELS.get(current_provider, DEFAULT_MODELS[DEFAULT_LLM_PROVIDER])
            model = questionary.text(f"Model to use (leave blank to use the default: {default_model}):").ask()
            config["MODEL"] = (model or "").strip()

        elif choice == "Web Search Provider":
            current_value = config.get("WEB_SEARCH_PROVIDER")
            web_search_provider = questionary.select(
                "Which web search provider would you like to use?",
                choices=[Choice(title=title, value=value) for title, value in WEB_SEARCH_PROVIDER_CHOICES.items()],
                default=current_value if current_value in WEB_SEARCH_PROVIDER_CHOICES.values() else None,
            ).ask()

            if web_search_provider and web_search_provider != current_value:
                config["WEB_SEARCH_PROVIDER"] = web_search_provider

                env_key = WEB_SEARCH_API_KEY_ENV.get(web_search_provider)
                if env_key:
                    prompt_credential(env_key)

        elif choice == "Communication Channels":
            prompt_channels(config)

        CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")

    print(f"Wrote {CONFIG_PATH}.")
    print_pending_warnings()


def validate_paths():
    """Docker bind-mounts CONFIG_PATH/ENV_PATH as files, but if the host path
    doesn't exist yet when the container starts, Docker silently creates a
    directory there instead of erroring — which then breaks every read/write
    below. Catch that case with an actionable message instead of a raw
    traceback."""
    broken = [p for p in (CONFIG_PATH, ENV_PATH) if p.is_dir()]

    if not broken:
        return

    names = " ".join(path.name for path in broken)
    print("Please run this where your docker-compose.yml is, then restart the container:")
    print(f"  rmdir {names}")
    print(f"  touch {names}")
    sys.exit(1)


def check_config():
    """Gate for any command that actually needs mosfet.config.json. Missing is fatal, invalid JSON is a warning (defaults are used instead)."""
    if not CONFIG_PATH.is_file():
        print("No config found. Run 'mosfet config' to set up Mosfet.")
        sys.exit(1)


def normalize_config_json():
    """If CONFIG_PATH is missing, empty, or isn't valid JSON, normalize it to "{}" so the rest of run_config() can just treat it as an ordinary empty config instead of a broken or absent file.
    """
    if not CONFIG_PATH.is_file():
        CONFIG_PATH.touch()

    content = CONFIG_PATH.read_text().strip()
    if content:
        try:
            json.loads(content)
            return
        except json.JSONDecodeError:
            pass

    CONFIG_PATH.write_text("{}\n")

def run_config():
    validate_paths()
    normalize_config_json()

    config = json.loads(CONFIG_PATH.read_text())

    if config:
        update_config()
    else:
        setup_config()
