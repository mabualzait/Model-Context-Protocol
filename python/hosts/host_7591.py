# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.3 Session Isolation and Security

class IsolatedMCPSession(MCPSession):
    def __init__(self, session_id: str, client_info: Dict, server_config: Dict, isolation_config: Dict):
        super().__init__(session_id, client_info, server_config)
        self.isolation_config = isolation_config
        self.security_context = {}
    
    def initialize(self):
        """Initialize isolated session"""
        # Set up isolation
        self._setup_isolation()
        
        # Initialize session
        return super().initialize()
    
    def _setup_isolation(self):
        """Set up session isolation"""
        # Create isolated namespace for resources
        if self.isolation_config.get("resource_isolation"):
            self.security_context["resource_namespace"] = f"session_{self.session_id}"
        
        # Set up access controls
        if self.isolation_config.get("access_control"):
            self.security_context["allowed_resources"] = self.isolation_config["allowed_resources"]
            self.security_context["allowed_tools"] = self.isolation_config["allowed_tools"]
    
    def validate_access(self, resource_uri: str = None, tool_name: str = None) -> bool:
        """Validate access to resource or tool"""
        if resource_uri:
            allowed_resources = self.security_context.get("allowed_resources", [])
            if allowed_resources and resource_uri not in allowed_resources:
                return False
        
        if tool_name:
            allowed_tools = self.security_context.get("allowed_tools", [])
            if allowed_tools and tool_name not in allowed_tools:
                return False
        
        return True
    
    def route_request(self, request: Dict) -> Dict:
        """Route request with access validation"""
        method = request.get("method", "")
        
        # Validate access
        if method.startswith("resources/"):
            uri = request.get("params", {}).get("uri")
            if uri and not self.validate_access(resource_uri=uri):
                raise PermissionError(f"Access denied to resource: {uri}")
        
        elif method.startswith("tools/"):
            tool_name = request.get("params", {}).get("name")
            if tool_name and not self.validate_access(tool_name=tool_name):
                raise PermissionError(f"Access denied to tool: {tool_name}")
        
        return super().route_request(request)