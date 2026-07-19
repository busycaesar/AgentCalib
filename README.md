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

<img width="611" height="528" alt="looks" src="https://github.com/user-attachments/assets/48a3bd6e-8c00-4440-b279-3384cc820fbf" />

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
 ├── adapters/   # Per-provider LLM adapters behind a common interface
 ├── config/     # Provider selection, seed messages, and shared paths
 ├── tools/      # Tool schemas and implementations available to the agent
 ├── utils/      # Shared helpers used across the codebase
 └── skills/     # Skill files live here
 scripts/
 └── install.sh # Installs Mosfet into ~/.mosfet and adds `mosfet` to PATH
```

## How to run the project?

### Option 1: Install script

```bash
curl -fsSL https://mosfet.shahtech.info | bash
```

This clones Mosfet, sets up an isolated Python environment, prompts for your OpenAI credentials, and installs a `mosfet` command on your `PATH`. Once it finishes, run the agent from anywhere:

```bash
mosfet
```

### Option 2: Manual setup (for development)

1. Create a virtual environment and install dependencies:

   ```bash
   pip install -r req.txt
   ```

2. Pick your provider and model in `src/config/provider.py` (`OpenAI`, `Ollama`, or `Anthropic`, plus `MODEL` and, depending on the provider, `BASE_URL` or `MAX_TOKENS`).

3. Copy the credentials for your chosen provider into a `.env` file at the project root (Ollama needs none):

   ```text
   OPENAI_API_KEY="..."
   OPENAI_ORG_ID="..."
   OPENAI_PROJECT="..."

   ANTHROPIC_API_KEY="..."
   ```

4. Run the agent:

   ```bash
   python src/main.py
   ```

## License

[MIT](LICENSE)

## Author

[Dev J. Shah](https://github.com/busycaesar)
