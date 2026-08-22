from abc import ABC, abstractmethod

class MCPClient(ABC):
    @abstractmethod
    def to_connection(self):
        """
        Describe this client's connection as a plain dict, for persisting to disk.
        """

    @abstractmethod
    def list_tools(self):
        """
        Fetch the tools this MCP server offers, in the server's own (raw) shape.
        """

    @abstractmethod
    def call_tool(self, tool_name, arguments):
        """
        Call one of this server's tools and return its result as text.
        """