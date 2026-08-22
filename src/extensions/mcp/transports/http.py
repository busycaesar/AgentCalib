import json
import httpx
from .base import MCPClient
from .protocol import build_payload, extract_call_result

class HTTPClient(MCPClient):
    def __init__(self, url):
        self.url = url

    def to_connection(self):
        return {"transport": "http", "url": self.url}

    def list_tools(self):
        return self._call("tools/list").get("tools", [])

    def call_tool(self, tool_name, arguments):
        params = {"name": tool_name, "arguments": arguments}
        response = self._call("tools/call", params)

        return extract_call_result(response, tool_name)

    def _call(self, method, params=None):
        payload = build_payload(method, params)

        response = httpx.post(self.url, json=payload, headers={"Accept": "application/json, text/event-stream"})

        response.raise_for_status()

        # Streamable HTTP servers may reply with plain JSON or with an SSE-framed body (`data: {...}`) for the same request — accept either.
        if "text/event-stream" in response.headers.get("content-type", ""):
            body = None
            for line in response.text.splitlines():
                if line.startswith("data:"):
                    body = json.loads(line[len("data:"):].strip())
                    break
            if body is None:
                raise RuntimeError(f"No data received from SSE response: {response.text}")
        else:
            body = response.json()

        if "error" in body:
            raise RuntimeError(body["error"]["message"])

        return body["result"]