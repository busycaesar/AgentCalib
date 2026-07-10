# AgentCalib

## Description

AgentCalib is an LLM-powered agent that you extend by adding **skills**, **tools** and **MCP Servers**. Each skill describes a capability or piece of knowledge the agent can draw on. The agent reads these skills and uses them to answer questions and carry out workflows, so the goal is to empower the LLM by simply dropping in more skill files.

> **Status: early-stage / work in progress.** The current codebase implements an OpenAI chat-completion agent with an interactive terminal chat loop, a `create_skill` tool the LLM can call to save new skills, and a `/skill_name` chat command that loads a saved skill back into the conversation. The agent can also chain multiple tool calls in a row before giving a final answer. MCP server support is not yet implemented.

## Tech Stack

![Image Alt](https://skillicons.dev/icons?i=python)

- Python

## AI Stack

- [OpenAI SDK](https://github.com/openai/openai-python)
- Model: `gpt-4o-mini`

## How it looks?

<img width="1365" height="616" alt="Screenshot From 2026-07-09 09-42-05" src="https://github.com/user-attachments/assets/fb59705c-4548-4517-b3d7-a0d32348df54" />

## Features

- [x] Basic chat-completion agent
- [x] Interactive terminal chat interface
- [x] Ask the agent to create a new skill, and it will do it for you
- [x] Skills — type `/skill_name` in chat to load a saved skill into the conversation
- [x] Agent chains multiple tool calls in a row before giving a final answer
- [x] Install script (`scripts/install.sh`) for a global `agentcalib` command
- [ ] MCP servers — connect MCP servers for the agent to use

## Using Skills

- Ask the agent to create one, e.g. "create a skill for writing commit messages" — it saves a new skill for later use.
- In any later chat, type `/<skill_name>` (matching the skill's name, case-sensitive) to load that skill's content into the conversation, e.g. `/commit fix the login bug`. Any text after the command is sent along as your actual request.
- If no skill matches the command, your message is sent through as normal chat text.

## Project Structure

```text
.
 src/
 ├── main.py           # Entry point
 ├── chat.py           # Interactive terminal chat loop
 ├── agent.py          # Talks to the OpenAI model, runs tool calls, loops until a final answer
 ├── skill_command.py  # Resolves a "/skill_name" chat command into skill file content
 ├── config/           # OpenAI client setup, seed messages, and shared paths
 ├── tools/             # Tool schemas and implementations available to the agent
 └── skills/            # Skill files live here, loaded via "/skill_name" in chat
 scripts/
 └── install.sh        # Installs AgentCalib into ~/.agentcalib and adds `agentcalib` to PATH
```

## How to run the project?

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
