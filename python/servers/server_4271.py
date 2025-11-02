# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.2 Server Lifecycle

class MCPServer:
    def __init__(self):
        self.state = {}
        self.resources = {}
        self.tools = {}
        self.prompts = {}
    
    def initialize(self, request):
        """Handle initialize request"""
        protocol_version = request.params.get("protocolVersion")
        client_capabilities = request.params.get("capabilities", {})
        client_info = request.params.get("clientInfo", {})
        
        # Store client info
        self.state["client"] = client_info
        self.state["client_capabilities"] = client_capabilities
        
        # Return server capabilities
        return {
            "protocolVersion": protocol_version,
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "serverInfo": {
                "name": "example-server",
                "version": "1.0.0"
            }
        }
    
    def handle_initialized(self, notification):
        """Handle initialized notification"""
        # Client is ready, server can now process requests
        self.state["initialized"] = True
    
    def shutdown(self, request):
        """Handle shutdown request"""
        # Clean up resources
        self.cleanup()
        return {}
    
    def cleanup(self):
        """Clean up server state"""
        self.state.clear()
        self.resources.clear()
        self.tools.clear()
        self.prompts.clear()