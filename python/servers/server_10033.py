# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.5 Troubleshooting Common Issues

class DebugToolExecution:
    """Debug tool execution issues."""
    
    def debug_tool_execution(self, server: 'MCPServer', tool_name: str, arguments: Dict):
        """Debug tool execution."""
        # Check if tool exists
        tools = server.list_tools()
        tool = next((t for t in tools if t.name == tool_name), None)
        
        if not tool:
            print(f"ERROR: Tool '{tool_name}' not found")
            print(f"Available tools: {[t.name for t in tools]}")
            return
        
        print(f"Tool found: {tool_name}")
        print(f"Tool description: {tool.description}")
        print(f"Tool schema: {json.dumps(tool.inputSchema, indent=2)}")
        
        # Validate arguments against schema
        schema = tool.inputSchema
        required = schema.get("properties", {}).keys()
        provided = set(arguments.keys())
        
        missing = set(schema.get("required", [])) - provided
        if missing:
            print(f"ERROR: Missing required arguments: {missing}")
            return
        
        # Try to execute tool
        try:
            result = server.call_tool(tool_name, arguments)
            print(f"✓ Tool executed successfully")
            print(f"Result: {result}")
        except Exception as e:
            print(f"✗ Tool execution failed: {e}")
            import traceback
            traceback.print_exc()