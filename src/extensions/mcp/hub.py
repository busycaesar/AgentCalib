import re
from .transports import create_mcp_client, create_mcp_client_from_input
from .translate import to_tool_schema, parse_mcp_tool_name
from .registry import get_available_mcp_servers, save_mcp_server, get_mcp_server_config

def get_mcp_tools():
    return [
        tool
        for server in get_available_mcp_servers()
        for tool in server.get("tools", [])
    ]

def add_mcp_server(server_name, url=None, command=None, args=None):
    mcp_client = create_mcp_client_from_input(url=url, command=command, args=args)
    return _register_mcp_server(server_name, mcp_client)

def call_tool_function(tool_name, args):
    server_name, real_tool_name = parse_mcp_tool_name(tool_name)

    server_config = get_mcp_server_config(server_name)

    if server_config is None:
        raise ValueError(f"No MCP tool named '{tool_name}'.")

    mcp_client = create_mcp_client(server_config)

    return mcp_client.call_tool(real_tool_name, args)

def update_mcp_server(name):
    """
    Update the tools list for the existing server.
    """
    existing = get_mcp_server_config(name)

    if existing is None:
        raise ValueError(f"No MCP server named '{name}' is configured.")

    alias = existing.get("alias", name)

    mcp_client = create_mcp_client(existing)

    return _register_mcp_server(alias, mcp_client)

def _register_mcp_server(server_name, mcp_client):
    # The name used as the config filename and tool-name prefix must be a single lowercase alphanumeric word (no separator characters, since "_" is what splits it back out of a tool name — see parse_mcp_tool_name). Whatever the caller passed in is kept as-is under "alias", purely for display.
    alias = server_name
    sanitized_name = re.sub(r"[^a-z0-9]", "", server_name.lower())

    if not sanitized_name:
        raise ValueError(f"'{server_name}' has no letters or digits to use as a server name.")

    available_tools = mcp_client.list_tools()

    # Convert each tool into the standard schema.
    available_tool_schemas = [
        to_tool_schema(sanitized_name, mcp_tool)
        for mcp_tool in available_tools
    ]

    connection = mcp_client.to_connection()

    save_mcp_server({"name": sanitized_name, "alias": alias, **connection, "tools": available_tool_schemas})

    # Return the list of tool (function) names.
    return [
        tool["function"]["name"]
        for tool in available_tool_schemas
    ]