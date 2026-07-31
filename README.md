<pre>
███╗   ███╗ ██████╗ ███████╗███████╗███████╗████████╗
████╗ ████║██╔═══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝
██╔████╔██║██║   ██║███████╗█████╗  █████╗     ██║
██║╚██╔╝██║██║   ██║╚════██║██╔══╝  ██╔══╝     ██║
██║ ╚═╝ ██║╚██████╔╝███████║██║     ███████╗   ██║
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚══════╝   ╚═╝
</pre>
 
## Description

Mosfet is an LLM-powered agent that you extend by adding **Skills**, **Tools** and **MCP Servers**. Each skill describes a capability or piece of knowledge the agent can draw on, tools let it take action, and MCP servers connect it to external systems. The goal is to empower the LLM by simply dropping in more of these building blocks.

> **Status: early-stage / work in progress.** The current codebase implements a chat-completion agent that is model-agnostic — you point it at whichever LLM provider and model you want to use, whether hosted or running locally — with an interactive terminal chat loop, a tool the LLM can call to save new skills, and a `/skill_name` chat command that loads a saved skill back into the conversation. The agent is also told what skills are available to it at the start of every conversation, and can decide on its own to load and follow one when it fits the request. The agent can chain multiple tool calls in a row before giving a final answer. MCP server support is not yet implemented.

## Tech Stack

![Image Alt](https://skillicons.dev/icons?i=python)

## AI Stack

- [OpenAI SDK](https://github.com/openai/openai-python)
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python)
- Model-agnostic: the provider and model are configurable, so you can run against a hosted or a local LLM

## How it looks?

### CLI
<img width="858" height="655" alt="looks" src="https://github.com/user-attachments/assets/c7d9209f-0587-4014-b399-63b220910920" />

### Discord
<img width="812" height="925" alt="discord" src="https://github.com/user-attachments/assets/8452443c-f662-4bcf-8e72-fe919f6cf7d3" />

## Features

- Chat with the agent right from your terminal
- Chat with the agent through direct messages on Discord
- Ask the agent to create a new skill, and it will save one for later use
- Bring a saved skill into a conversation whenever you need it
- The agent knows which skills it has available and can recognize on its own when one applies, loading it without you having to ask
- The agent can work through multiple steps on its own before giving you a final answer
- The agent can search the web and read pages to answer questions that need current or specific information
- Point the agent at whichever LLM provider and model you want, hosted or local
- Set up or change your provider, model, and credentials anytime through a short guided prompt
- Install once and run the agent from anywhere on your machine

## Project Structure

```text
.
 src/
 ├── main.py            # Entry point
 ├── config_setup.py    # Guided setup/update for provider config and credentials
 ├── communications.py  # Picks and launches the configured front-end
 ├── core/       # Agent loop and skill/tool orchestration
 ├── adapters/   # Per-provider LLM and web-search adapters behind common interfaces
 │    ├── llm_providers/
 │    └── web_search_providers/
 ├── config/     # Provider selection, seed messages, and shared paths
 ├── extensions/ # Tools (and eventually skills/MCP) available to the agent
 │    ├── skills/
 │    └── tools/
 ├── ui/         # Front-ends: terminal chat loop and Discord bot
 └── utils/      # Shared helpers used across the codebase
 scripts/
 └── install.sh # Installs Mosfet into ~/.mosfet and adds `mosfet` to PATH
```

## How to run the project?

### Option 1: Install script

```bash
bash <(curl -fsSL https://mosfet.shahtech.info)
```

This clones the latest Mosfet release, sets up an isolated Python environment, and installs a `mosfet` command on your `PATH`. Once it finishes, set up your provider and credentials, then start chatting:

```bash
mosfet config
mosfet
```

### Option 2: Manual setup (for development)

1. Create a virtual environment and install dependencies:

   ```bash
   pip install -r req.txt
   ```

2. Set up your provider and credentials:

   ```bash
   python3 src/main.py config
   ```

   This walks you through picking an LLM provider, model, and web search provider, and prompts for whichever credentials you need — writing `mosfet.config.json` and `.env` for you. Run it again anytime to change your setup. Rarely-changed settings like Ollama's server URL or Anthropic's response length cap live in `src/config/advanced_providers.py` if you ever need to adjust them.

3. Run the agent:

   ```bash
   python src/main.py
   ```

## License

[MIT](LICENSE)

## Author

[Dev J. Shah](https://github.com/busycaesar)
</pre>