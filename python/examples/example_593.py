# 📖 Chapter: Chapter 1: Introduction to Model Context Protocol
# 📖 Section: 1.8 Technical Deep Dive: How MCP Works

# Step 1: Client sends tool call request
{
    "jsonrpc": "2.0",
    "id": 123,
    "method": "tools/call",
    "params": {
        "name": "read_file",
        "arguments": {
            "path": "/path/to/file.txt"
        }
    }
}

# Step 2: Server processes request
def handle_tool_call(name, arguments):
    if name == "read_file":
        with open(arguments["path"], 'r') as f:
            content = f.read()
        return {"content": [{"type": "text", "text": content}]}

# Step 3: Server sends response
{
    "jsonrpc": "2.0",
    "id": 123,
    "result": {
        "content": [
            {
                "type": "text",
                "text": "File contents here..."
            }
        ],
        "isError": false
    }
}

# Step 4: Client receives and processes response
response = await client.call_tool("read_file", {"path": "/path/to/file.txt"})
content = response["content"][0]["text"]