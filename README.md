# AgentCalib

## Description

AgentCalib is an LLM-powered agent that you extend by adding **skills**, **tools** and **MCP Servers**. Each skill describes a capability or piece of knowledge the agent can draw on. The agent reads these skills and uses them to answer questions and carry out workflows, so the goal is to empower the LLM by simply dropping in more skill files.

> **Status: early-stage / work in progress.** The current codebase implements an OpenAI chat-completion agent with an interactive terminal chat loop and one function-calling tool, which lets the LLM create a new skill on request. Nothing reads those skills back into the agent's context yet. MCP server support is not yet implemented.

## Tech Stack

![Image Alt](https://skillicons.dev/icons?i=python)

- Python

## AI Stack

- [OpenAI SDK](https://github.com/openai/openai-python)
- Model: `gpt-4o-mini`
- Function calling (tools) for agent actions

## How it looks?

## Features

- [x] Basic chat-completion agent
- [x] Interactive terminal chat interface
- [x] Ask the agent to create a new skill, and it will do it for you
- [ ] Skills — agent does not yet read skills back into its context
- [ ] MCP servers — connect MCP servers for the agent to use

## Project Structure

```text
.
├── src/
│   ├── main.py    # Entry point
│   ├── chat.py    # Interactive terminal chat loop
│   ├── agent.py   # Talks to the OpenAI model and runs tool calls it requests
│   ├── config/    # OpenAI client setup, seed messages, and shared paths
│   ├── tools/     # Tool schemas and implementations available to the agent
│   └── skills/    # Skill files live here (currently empty; not yet read by the agent)
└── README.md
```

## How to run the project?

1. Create a virtual environment and install dependencies from `req.txt`:

   ```bash
   pip install -r req.txt
   ```

2. Copy `.env.example` to `.env` at the project root, then fill in your OpenAI credentials:

   ```bash
   cp .env.example .env
   ```

3. Run the agent:

   ```bash
   python src/main.py
   ```

## Author

[Dev J. Shah](https://github.com/busycaesar)
