# Shared, transport-agnostic pieces of talking to an MCP server — the JSON-RPC envelope (same for HTTP and stdio under the 2026-07-28 stateless spec, since both just carry protocol version/capabilities in params._meta) and pulling text back out of a tools/call result.

PROTOCOL_VERSION = "2026-07-28"
CLIENT_INFO = {"name": "mosfet", "version": "0.6.0"}

def build_payload(method, params=None):
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            **(params or {}),
            "_meta": {
                "io.modelcontextprotocol/protocolVersion": PROTOCOL_VERSION,
                "io.modelcontextprotocol/clientCapabilities": {},
                "io.modelcontextprotocol/clientInfo": CLIENT_INFO,
            },
        },
    }

def extract_call_result(response, tool_name):
    if response.get("isError"):
        return f"Error calling {tool_name}: {response}"

    content_blocks = response.get("content", [])

    return "\n".join(block.get("text", "") for block in content_blocks if block.get("type") == "text")