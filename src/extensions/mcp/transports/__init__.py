from .http import HTTPClient
from .stdio import StdioClient

def create_mcp_client_from_input(url=None, command=None, args=None):
    if url:
        return create_mcp_client({"transport": "http", "url": url})
    elif command:
        return create_mcp_client({"transport": "stdio", "command": command, "args": args or []})
    else:
        raise ValueError("Provide either a url (HTTP server) or a command (stdio server).")

def create_mcp_client(server):
    if server["transport"] == "http":
        return HTTPClient(server["url"])
    elif server["transport"] == "stdio":
        return StdioClient(server["command"], server.get("args") or [])
    else:
        raise ValueError(f"No MCP transport implemented for '{server['transport']}'.")