# Mosfet

<img width="1000" height="250" alt="banner" src="https://github.com/user-attachments/assets/d4bd7925-6fdd-4152-826a-23a8d6ca0ca2" />

## Description

Mosfet is an LLM-powered agent that you extend by adding **Skills**, **Tools** and **MCP Servers**. Each skill describes a capability or piece of knowledge the agent can draw on, tools let it take action, and MCP servers connect it to external systems. The goal is to empower the LLM by simply dropping in more of these building blocks.

> **Status: early-stage / work in progress.** The current codebase implements an OpenAI chat-completion agent with an interactive terminal chat loop, a `create_skill` tool the LLM can call to save new skills, and a `/skill_name` chat command that loads a saved skill back into the conversation. The agent can also chain multiple tool calls in a row before giving a final answer. MCP server support is not yet implemented.

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

## Skills

### CreateSkill

This skill helps an LLM (Large Language Model) to create new skills by providing step-by-step instructions. It outlines the process of skill creation, including defining objectives, writing content, and setting up functionality.

#### Instructions

1. **Define the Skill's Purpose**:
   - Determine what the skill should accomplish. Identify the target audience and the primary function that the skill will serve.

2. **Draft the Skill Content**:
   - Write the core content of the skill, including detailed descriptions, instructions, and any necessary contextual information that the skill will require to function effectively.

3. **Specify Input/Output Requirements**:
   - Define what input the skill will require from users and what output it should provide in response.

4. **Include Error Handling**:
   - Implement strategies for managing potential errors or miscommunications, ensuring the skill can gracefully handle unexpected input or situations.

5. **Test the Skill**:
   - Conduct thorough testing to ensure that the skill operates as intended. Test with different inputs and scenarios to validate its functionality.

6. **Optimize and Refine**:
   - Refine the skill based on testing feedback. Optimize the content and functionalities to enhance user experience and operational efficiency.

7. **Publish the Skill**:
   - Prepare the skill for deployment. Follow the necessary protocols or guidelines for making the skill available for use within the relevant system.

8. **Document the Skill**:
   - Create comprehensive documentation, including usage instructions, API references, and troubleshooting tips, to ensure users understand how to effectively interact with the skill.

#### Example

**Skill Name:** WeatherInfo  
**Purpose:** Provide weather information based on user location.  
**Content:** Retrieves current raining status, humidity level, and temperature.  
**Inputs:** User's geographical location.  
**Outputs:** Current weather status and forecast for the next 3 days.