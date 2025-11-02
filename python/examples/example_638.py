# 📖 Chapter: Chapter 1: Introduction to Model Context Protocol
# 📖 Section: 1.8 Technical Deep Dive: How MCP Works

class MCPSession:
    """Stateful MCP session."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.state = {
            "authenticated": False,
            "capabilities": {},
            "resources": [],
            "tools": [],
            "subscriptions": {},
            "context": {}
        }
    
    def initialize(self, client_info: Dict, server_capabilities: Dict):
        """Initialize session with client and server capabilities."""
        self.state["client_info"] = client_info
        self.state["capabilities"] = server_capabilities
        self.state["authenticated"] = True
    
    def subscribe_resource(self, uri: str):
        """Subscribe to resource updates."""
        self.state["subscriptions"][uri] = True
    
    def update_context(self, key: str, value: Any):
        """Update session context."""
        self.state["context"][key] = value