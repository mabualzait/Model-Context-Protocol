# 📖 Chapter: Chapter 15: The Future of MCP
# 📖 Section: 15.3 Community and Ecosystem Growth

# Official Python MCP SDK example
from mcp import MCPServer, MCPClient
from mcp.types import Resource, Tool

# Server implementation
server = MCPServer("my-server")

@server.resource("file://*")
def file_resource(uri: str) -> Resource:
    """Provide file as resource."""
    return Resource(uri=uri, name=uri.split('/')[-1])

@server.tool("read_file")
def read_file(path: str) -> str:
    """Read file tool."""
    with open(path, 'r') as f:
        return f.read()

# Client implementation
client = MCPClient("http://localhost:8080")
client.connect()

resources = client.list_resources()
content = client.read_resource("file://example.txt")
result = client.call_tool("read_file", {"path": "example.txt"})