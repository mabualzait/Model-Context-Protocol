# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.7 Advanced Client Patterns

class MultiServerMCPClient:
    """Client that manages connections to multiple MCP servers."""
    
    def __init__(self):
        self.clients: Dict[str, 'MCPClient'] = {}
        self.server_capabilities: Dict[str, Dict] = {}
    
    def connect_to_server(self, server_id: str, endpoint: str, transport: str = "stdio"):
        """Connect to an MCP server."""
        client = MCPClient(endpoint, transport=transport)
        client.connect()
        
        self.clients[server_id] = client
        
        # Discover server capabilities
        capabilities = {
            "resources": client.list_resources(),
            "tools": client.list_tools(),
            "prompts": client.list_prompts()
        }
        self.server_capabilities[server_id] = capabilities
    
    def find_tool(self, tool_name: str) -> Optional[str]:
        """Find which server has the tool."""
        for server_id, capabilities in self.server_capabilities.items():
            tools = capabilities.get("tools", [])
            if any(tool.get("name") == tool_name for tool in tools):
                return server_id
        return None
    
    def call_tool_anywhere(self, tool_name: str, arguments: Dict) -> Dict:
        """Call tool on any server that has it."""
        server_id = self.find_tool(tool_name)
        
        if not server_id:
            raise ValueError(f"Tool not found on any server: {tool_name}")
        
        client = self.clients[server_id]
        return client.call_tool(tool_name, arguments)
    
    def aggregate_resources(self) -> List[Dict]:
        """Aggregate resources from all servers."""
        all_resources = []
        
        for server_id, capabilities in self.server_capabilities.items():
            resources = capabilities.get("resources", [])
            for resource in resources:
                resource["server_id"] = server_id
                all_resources.append(resource)
        
        return all_resources