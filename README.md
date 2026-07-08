# AgentCalib

## Description

AgentCalib is an LLM-powered agent that you extend by adding **skills** — plain `.md` files placed in `src/skills/`. Each skill describes a capability or piece of knowledge the agent can draw on. The agent reads these skills and uses them to answer questions and carry out workflows, so the goal is to empower the LLM by simply dropping in more skill files.

> **Status: early-stage / work in progress.** The current codebase implements a minimal OpenAI chat-completion agent (`src/agent.py`) with a static message list. The `src/skills/` directory exists but is currently empty. There is no chat interface yet for interacting with the agent or testing skills — that's the next piece to be built.

## Tech Stack

![Image Alt](https://skillicons.dev/icons?i=python)

- Python
- [OpenAI SDK](https://github.com/openai/openai-python)

## How it looks?

## Features

- [x] Basic OpenAI chat-completion agent
- [ ] Skills — add `.md` files to `src/skills/` for the agent to use
- [ ] Chat interface to interact with the agent and test skills

## How to run the project?

1. Create a virtual environment and install dependencies (`openai`, `python-dotenv`).
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

## Author

[Dev J. Shah](https://github.com/busycaesar)
