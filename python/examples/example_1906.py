# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.7 Advanced Architectural Patterns

class CascadingMCPServer:
    """MCP server that delegates to other servers."""
    
    def __init__(self):
        self.upstream_servers: List['MCPClient'] = []
    
    def call_tool(self, name: str, arguments: Dict) -> Dict:
        """Call tool, delegating to upstream servers if needed."""
        # Check if we handle this tool
        if name in self.local_tools:
            return self._execute_local_tool(name, arguments)
        
        # Delegate to upstream servers
        for server in self.upstream_servers:
            try:
                if name in server.list_tools():
                    return server.call_tool(name, arguments)
            except:
                continue
        
        raise ValueError(f"Tool {name} not found")