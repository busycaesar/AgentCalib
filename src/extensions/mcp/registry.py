import json
from config import MCP_SERVERS_PATH

def get_available_mcp_servers():
    if not MCP_SERVERS_PATH.is_dir():
        return []
        
    return [
        json.loads(config_file.read_text()) 
        for config_file in MCP_SERVERS_PATH.glob("*.json")
    ]

def get_mcp_server_config(name):
    config_file = MCP_SERVERS_PATH / f"{name}.json"

    if not config_file.is_file():
        return None

    return json.loads(config_file.read_text())

def save_mcp_server(server):
    # `server` already has whatever fields its transport needs (url for http; command/args for stdio) plus name/tools — registry.py just persists it.
    MCP_SERVERS_PATH.mkdir(parents=True, exist_ok=True)
    config_file = MCP_SERVERS_PATH / f"{server['name']}.json"
    config_file.write_text(json.dumps(server, indent=2) + "\n")