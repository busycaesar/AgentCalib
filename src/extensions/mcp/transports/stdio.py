import json
import subprocess
from .base import MCPClient
from .protocol import build_payload, extract_call_result

class StdioClient(MCPClient):
    def __init__(self, command, args):
        self.command = command
        self.args = args

    def to_connection(self):
        return {"transport": "stdio", "command": self.command, "args": self.args}

    def list_tools(self):
        return self._call("tools/list").get("tools", [])

    def call_tool(self, tool_name, arguments):
        params = {"name": tool_name, "arguments": arguments}
        response = self._call("tools/call", params)

        return extract_call_result(response, tool_name)

    # Spawns the server process fresh for this one call, writes a single JSON-RPC message to its stdin, reads a single line back from its stdout, then terminates the process — no persistent process kept around between calls, matching the HTTP transport's "no state" model.
    def _call(self, method, params=None):
        payload = build_payload(method, params)

        process = subprocess.Popen(
            [self.command, *self.args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        try:
            process.stdin.write(json.dumps(payload) + "\n")
            process.stdin.flush()

            # Per spec, the server MUST NOT write anything to stdout that
            # isn't a valid MCP message, so the first line is the response.
            response_line = process.stdout.readline()
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

        if not response_line:
            raise RuntimeError(f"MCP server process '{self.command}' produced no response: {process.stderr.read()}")

        body = json.loads(response_line)

        if "error" in body:
            raise RuntimeError(body["error"]["message"])

        return body["result"]
