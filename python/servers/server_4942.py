# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.7 Best Practices for Server Design

def call_tool(self, name, arguments):
    try:
        result = self._execute_tool(name, arguments)
        return {"content": [{"type": "text", "text": result}], "isError": False}
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error: {str(e)}"}],
            "isError": True
        }