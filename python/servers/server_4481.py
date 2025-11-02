# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.4 Tools: Exposing Executable Functions

def call_tool(self, name, arguments):
    if name == "read_file":
        path = arguments.get("path")
        with open(path, 'r') as f:
            content = f.read()
        return {
            "content": [
                {"type": "text", "text": content}
            ],
            "isError": False
        }
    else:
        return {
            "content": [
                {"type": "text", "text": f"Unknown tool: {name}"}
            ],
            "isError": True
        }