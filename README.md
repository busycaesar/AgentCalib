# Mosfet

<img width="1000" height="250" alt="banner" src="https://github.com/user-attachments/assets/d4bd7925-6fdd-4152-826a-23a8d6ca0ca2" />

## Description

Mosfet is an LLM-powered agent that you extend by adding **Skills**, **Tools** and **MCP Servers**. Each skill describes a capability or piece of knowledge the agent can draw on, tools let it take action, and MCP servers connect it to external systems. The goal is to empower the LLM by simply dropping in more of these building blocks.

> **Status: early-stage / work in progress.** The current codebase implements an OpenAI chat-completion agent with an interactive terminal chat loop, a tool the LLM can call to save new skills, and a `/skill_name` chat command that loads a saved skill back into the conversation. The agent is also told what skills are available to it at the start of every conversation, and can decide on its own to load and follow one when it fits the request. The agent can chain multiple tool calls in a row before giving a final answer. MCP server support is not yet implemented.

## Tech Stack

![Image Alt](https://skillicons.dev/icons?i=python)

## AI Stack

- [OpenAI SDK](https://github.com/openai/openai-python)
- Model: `gpt-4o-mini`

## How it looks?

<img width="1365" height="616" alt="Screenshot From 2026-07-09 09-42-05" src="https://github.com/user-attachments/assets/fb59705c-4548-4517-b3d7-a0d32348df54" />

## Features

- Chat with the agent right from your terminal
- Ask the agent to create a new skill, and it will save one for later use
- Bring a saved skill into a conversation whenever you need it
- The agent knows which skills it has available and can recognize on its own when one applies, loading it without you having to ask
- The agent can work through multiple steps on its own before giving you a final answer
- Install once and run the agent from anywhere on your machine

## Project Structure

```text
.
 src/
 ├── main.py    # Entry point
 ├── chat.py    # Interactive terminal chat loop
 ├── core/      # Agent loop and skill/tool orchestration
 ├── config/    # OpenAI client setup, seed messages, and shared paths
 ├── tools/     # Tool schemas and implementations available to the agent
 └── skills/    # Skill files live here
 scripts/
 └── install.sh # Installs Mosfet into ~/.mosfet and adds `mosfet` to PATH
```

## How to run the project?

### Option 1: Install script

```bash
bash scripts/install.sh
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

2. Copy your OpenAI credentials into a `.env` file at the project root:

   ```text
   OPENAI_API_KEY="..."
   OPENAI_ORG_ID="..."
   OPENAI_PROJECT="..."
   ```

3. Run the agent:

   ```bash
   python src/main.py
   ```

## License

[MIT](LICENSE)

## Author

[Dev J. Shah](https://github.com/busycaesar)
