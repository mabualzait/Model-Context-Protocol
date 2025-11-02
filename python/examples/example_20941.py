# 📖 Chapter: Appendices
# 📖 Section: E.1 Common MCP Patterns

# List available tools
tools = client.list_tools()
for tool in tools:
    print(f"{tool['name']}: {tool['description']}")

# Call tool with arguments
result = client.call_tool("read_file", {"path": "/path/to/file.txt"})

# Handle tool errors
try:
    result = client.call_tool("write_file", {"path": "...", "content": "..."})
    if result.get("isError"):
        print(f"Error: {result['content'][0]['text']}")
except Exception as e:
    print(f"Tool call failed: {e}")