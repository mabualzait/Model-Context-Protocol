# 📖 Chapter: Chapter 3: MCP in the Ecosystem
# 📖 Section: 3.9 Building Ecosystem-Aware Applications

class EcosystemAwareMCPServer(MCPServer):
    """MCP server designed for ecosystem compatibility."""
    
    def __init__(self, name: str, version: str):
        super().__init__(name, version)
        
        # Ensure compatibility
        self.protocol_version = "2024-11-05"  # Latest stable version
        
        # Support standard capabilities
        self.capabilities = {
            "tools": {},
            "resources": {},
            "prompts": {}
        }
    
    def initialize(self, request: Dict) -> Dict:
        """Initialize with ecosystem awareness."""
        client_capabilities = request.get("capabilities", {})
        client_info = request.get("clientInfo", {})
        
        # Log client info for ecosystem analysis
        logger.info(f"Client: {client_info.get('name')} v{client_info.get('version')}")
        
        # Negotiate capabilities
        negotiated_capabilities = self._negotiate_capabilities(client_capabilities)
        
        return {
            "protocolVersion": self.protocol_version,
            "capabilities": negotiated_capabilities,
            "serverInfo": {
                "name": self.name,
                "version": self.version
            }
        }
    
    def _negotiate_capabilities(self, client_capabilities: Dict) -> Dict:
        """Negotiate capabilities with client."""
        # Support standard capabilities that all clients should support
        negotiated = {}
        
        # Always support tools
        if "tools" in client_capabilities or True:
            negotiated["tools"] = {}
        
        # Always support resources
        if "resources" in client_capabilities or True:
            negotiated["resources"] = {}
        
        # Conditionally support prompts if client supports them
        if "prompts" in client_capabilities:
            negotiated["prompts"] = {}
        
        return negotiated
    
    def list_tools(self) -> Dict:
        """List tools with clear descriptions."""
        return {
            "tools": [
                {
                    "name": "standard_tool",
                    "description": "Clear, concise description for ecosystem compatibility",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "param": {
                                "type": "string",
                                "description": "Clear parameter description"
                            }
                        },
                        "required": ["param"]
                    }
                }
            ]
        }