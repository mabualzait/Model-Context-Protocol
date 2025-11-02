# 📖 Chapter: Chapter 3: MCP in the Ecosystem
# 📖 Section: 3.9 Building Ecosystem-Aware Applications

class EcosystemAwareMCPClient(MCPClient):
    """MCP client designed for ecosystem compatibility."""
    
    def __init__(self, endpoint: str, transport: str = "stdio"):
        super().__init__(endpoint, transport)
        
        # Support multiple protocol versions
        self.supported_versions = ["2024-11-05"]
        self.current_version = None
    
    async def connect(self):
        """Connect with version negotiation."""
        # Initialize with preferred version
        init_response = await self._initialize({
            "protocolVersion": self.supported_versions[0],
            "capabilities": {
                "tools": {},
                "resources": {},
                "prompts": {}
            },
            "clientInfo": {
                "name": "ecosystem-client",
                "version": "1.0.0"
            }
        })
        
        # Negotiate to server's supported version
        self.current_version = init_response.get("protocolVersion")
        
        if self.current_version not in self.supported_versions:
            logger.warning(f"Server version {self.current_version} may not be fully supported")
        
        # Send initialized notification
        await self._send_notification("notifications/initialized", {})
        
        return init_response
    
    async def discover_capabilities(self) -> Dict:
        """Discover server capabilities."""
        capabilities = {}
        
        try:
            # Try to list tools
            tools = await self.list_tools()
            capabilities["tools"] = len(tools)
        except Exception as e:
            logger.warning(f"Server does not support tools: {e}")
        
        try:
            # Try to list resources
            resources = await self.list_resources()
            capabilities["resources"] = len(resources)
        except Exception as e:
            logger.warning(f"Server does not support resources: {e}")
        
        try:
            # Try to list prompts
            prompts = await self.list_prompts()
            capabilities["prompts"] = len(prompts)
        except Exception as e:
            logger.warning(f"Server does not support prompts: {e}")
        
        return capabilities