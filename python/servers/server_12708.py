# 📖 Chapter: Chapter 9: Advanced MCP Patterns
# 📖 Section: 9.1 Multi-Server Architectures

class SmartMCPRouter:
    """Route requests to appropriate MCP servers based on capability."""
    
    def __init__(self, multi_client: MultiServerMCPClient):
        self.multi_client = multi_client
        self.server_capabilities: Dict[str, set] = {}
        self._build_capability_map()
    
    def _build_capability_map(self):
        """Build map of server capabilities."""
        all_tools = self.multi_client.list_all_tools()
        all_resources = self.multi_client.list_all_resources()
        
        for server_id, tools in all_tools.items():
            capabilities = set()
            
            # Add tool capabilities
            for tool in tools:
                capabilities.add(f"tool:{tool['name']}")
                if 'description' in tool:
                    # Extract keywords from description
                    keywords = self._extract_keywords(tool['description'])
                    capabilities.update(keywords)
            
            # Add resource capabilities
            for resource in all_resources.get(server_id, []):
                uri = resource.get('uri', '')
                if uri.startswith('file://'):
                    capabilities.add('resource:filesystem')
                elif uri.startswith('db://'):
                    capabilities.add('resource:database')
                elif uri.startswith('api://'):
                    capabilities.add('resource:api')
            
            self.server_capabilities[server_id] = capabilities
    
    def _extract_keywords(self, text: str) -> set:
        """Extract capability keywords from text."""
        keywords = {
            'search', 'query', 'database', 'file', 'web', 'api',
            'email', 'calendar', 'document', 'code', 'test'
        }
        
        text_lower = text.lower()
        found = set()
        
        for keyword in keywords:
            if keyword in text_lower:
                found.add(keyword)
        
        return found
    
    def route_request(self, capability: str, operation: str = None) -> Optional[str]:
        """Route request to server with required capability."""
        # Exact capability match
        for server_id, capabilities in self.server_capabilities.items():
            if capability in capabilities:
                return server_id
            
            # Check if operation-specific capability exists
            if operation:
                op_capability = f"{operation}:{capability}"
                if op_capability in capabilities:
                    return server_id
        
        # Fuzzy match
        for server_id, capabilities in self.server_capabilities.items():
            if any(cap.startswith(capability) for cap in capabilities):
                return server_id
        
        return None
    
    def route_tool_call(self, tool_name: str, arguments: Dict) -> Dict:
        """Route tool call to appropriate server."""
        server_id = self.route_request(f"tool:{tool_name}")
        
        if not server_id:
            return {
                'status': 'error',
                'message': f'No server found with tool: {tool_name}'
            }
        
        try:
            result = self.multi_client.servers[server_id].call_tool(
                tool_name, arguments
            )
            return {
                'status': 'success',
                'server_id': server_id,
                'result': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'server_id': server_id,
                'error': str(e)
            }