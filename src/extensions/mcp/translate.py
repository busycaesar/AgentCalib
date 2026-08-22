MCP_TOOL_NAME_PREFIX = "mcp"

def encode_mcp_tool_name(server_name, tool_name):
    return f"{MCP_TOOL_NAME_PREFIX}_{server_name}_" + tool_name

def is_mcp_tool(tool_name):
    return tool_name.startswith(MCP_TOOL_NAME_PREFIX)

def parse_mcp_tool_name(tool_name):
    # Server names are enforced to contain no underscores (see add_mcp_server), so "mcp_<servername>_<real_tool_name>" splits unambiguously in one pass.
    if not is_mcp_tool(tool_name):
        raise ValueError(f"'{tool_name}' is not an MCP tool name.")

    _, server_name, real_tool_name = tool_name.split("_", 2)

    return server_name, real_tool_name

def to_tool_schema(server_name, mcp_tool):
    return {
        "type": "function",
        "function": {
            "name": encode_mcp_tool_name(server_name, mcp_tool["name"]),
            "description": mcp_tool.get("description", ""),
            "parameters": mcp_tool.get("inputSchema", {"type": "object", "properties": {}}),
            # No "strict": True. Strict mode requires every parameter to be required, and forcing that onto other servers' schemas would mean rewriting each one ourselves and making the LLM guess values instead of relying on the server's own defaults.
        },
    }