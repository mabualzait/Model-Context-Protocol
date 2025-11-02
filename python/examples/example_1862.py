# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.7 Advanced Architectural Patterns

class MultiServerHost:
    """Host managing multiple MCP servers."""
    
    def __init__(self):
        self.servers: Dict[str, 'MCPServerConnection'] = {}
        self.server_capabilities: Dict[str, set] = {}
    
    def register_server(self, server_id: str, connection: 'MCPServerConnection'):
        """Register a new MCP server."""
        self.servers[server_id] = connection
        
        # Discover server capabilities
        capabilities = connection.discover_capabilities()
        self.server_capabilities[server_id] = capabilities
    
    def route_request(self, request: Dict) -> str:
        """Route request to appropriate server."""
        method = request.get("method")
        
        # Route based on method namespace
        if method.startswith("tools/"):
            return self._route_tool_request(request)
        elif method.startswith("resources/"):
            return self._route_resource_request(request)
        else:
            return self._route_general_request(request)
    
    def _route_tool_request(self, request: Dict) -> str:
        """Route tool request to server with that tool."""
        tool_name = request.get("params", {}).get("name")
        
        # Find server with this tool
        for server_id, capabilities in self.server_capabilities.items():
            if tool_name in capabilities.get("tools", []):
                return server_id
        
        raise ValueError(f"No server found with tool: {tool_name}")