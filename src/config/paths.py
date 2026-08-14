from pathlib import Path

SKILLS_DIR = "extensions/skills"
SKILLS_INDEX_FILE = "index.json"
CONFIG_FILE = "mosfet.config.json"
ENV_FILE = ".env"
MCP_SERVERS_DIR = "extensions/mcp/servers"

SKILLS_PATH = Path(__file__).resolve().parent.parent / SKILLS_DIR
SKILLS_INDEX_PATH = SKILLS_PATH / SKILLS_INDEX_FILE
MCP_SERVERS_PATH = Path(__file__).resolve().parent.parent / MCP_SERVERS_DIR

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / CONFIG_FILE
ENV_PATH = Path(__file__).resolve().parent.parent.parent / ENV_FILE