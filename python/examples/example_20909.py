# 📖 Chapter: Appendices
# 📖 Section: E.1 Common MCP Patterns

# Client initialization
from mcp import MCPClient

client = MCPClient("http://localhost:8080", transport="http")
client.connect()

# Server initialization response
{
  "protocolVersion": "2024-11-05",
  "capabilities": {},
  "serverInfo": {"name": "my-server", "version": "1.0.0"}
}