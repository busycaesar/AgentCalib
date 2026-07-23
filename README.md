# Mosfet

<img width="1000" height="250" alt="mosfet" src="https://github.com/user-attachments/assets/665d93f4-fe6d-4e2c-8195-67a266f7e244" />

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

<img width="858" height="655" alt="looks" src="https://github.com/user-attachments/assets/c7d9209f-0587-4014-b399-63b220910920" />

## Features

- Chat with the agent right from your terminal
- Ask the agent to create a new skill, and it will save one for later use
- Bring a saved skill into a conversation whenever you need it
- The agent knows which skills it has available and can recognize on its own when one applies, loading it without you having to ask
- The agent can work through multiple steps on its own before giving you a final answer
- The agent can search the web and read pages to answer questions that need current or specific information
- Point the agent at whichever LLM provider and model you want, hosted or local
- Install once and run the agent from anywhere on your machine

## Project Structure

```text
.
 src/
 ├── main.py     # Entry point
 ├── cli.py      # Interactive terminal chat loop
 ├── core/       # Agent loop and skill/tool orchestration
 ├── adapters/   # Per-provider LLM and web-search adapters behind common interfaces
 │    ├── llm_providers/
 │    └── web_search_providers/
 ├── config/     # Provider selection, seed messages, and shared paths
 ├── extensions/ # Tools (and eventually skills/MCP) available to the agent
 │    ├── skills/
 │    └── tools/
 └── utils/      # Shared helpers used across the codebase
 scripts/
 └── install.sh # Installs Mosfet into ~/.mosfet and adds `mosfet` to PATH
```

## How to run the project?

### Option 1: Install script

```bash
bash <(curl -fsSL https://mosfet.shahtech.info)
```

This clones the latest Mosfet release, sets up an isolated Python environment, prompts you to pick an LLM provider and web search provider (with credentials for whichever you choose), and installs a `mosfet` command on your `PATH`. Once it finishes, run the agent from anywhere:

```bash
mosfet
```

### Option 2: Manual setup (for development)

1. Create a virtual environment and install dependencies:

   ```bash
   pip install -r req.txt
   ```

2. Copy `mosfet.config.example.json` to `mosfet.config.json` at the project root, and set `LLM_PROVIDER` (`OpenAI`, `Ollama`, or `Anthropic`), `MODEL`, and `WEB_SEARCH_PROVIDER` (`DuckDuckGo`, which needs no key, or `Brave`). Rarely-changed settings like Ollama's server URL or Anthropic's response length cap live in `src/config/advanced_providers.py` if you ever need to adjust them.

3. Copy the credentials for your chosen provider(s) into a `.env` file at the project root (Ollama and DuckDuckGo need none):

   ```text
   OPENAI_API_KEY="..."

   ANTHROPIC_API_KEY="..."

   BRAVE_API_KEY="..."
   ```

4. Run the agent:

   ```bash
   python src/main.py
   ```

## License

[MIT](LICENSE)

## Author

[Dev J. Shah](https://github.com/busycaesar)
