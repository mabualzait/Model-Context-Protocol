# 📖 Chapter: Chapter 3: MCP in the Ecosystem
# 📖 Section: 3.2 Integration with Major AI Models

# GPT-4 with MCP (planned)
import openai
from mcp_client import MCPClient

client = openai.OpenAI()
mcp_client = MCPClient("filesystem-server")

# GPT-4 can now use MCP servers
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Read file.txt"}],
    mcp_servers=[mcp_client]
)