# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.4 Tool Invocation Patterns

class MCPClient:
    def list_tools(self):
        """List all available tools"""
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "tools/list"
        }
        
        response = self._send_request(request)
        
        if response.get("error"):
            raise ValueError(f"Failed to list tools: {response['error']}")
        
        tools = response["result"].get("tools", [])
        
        # Update session state
        for tool in tools:
            self.session.add_tool(tool)
        
        return tools