# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.1 Adding MCP Support to Existing Applications

from mcp_host import MCPHost

class MyHostApplication:
    """Application with MCP host integration."""
    
    def __init__(self):
        self.host = MCPHost()
        self.sessions: Dict[str, str] = {}  # user_id -> session_id
    
    def create_user_session(self, user_id: str, server_configs: List[Dict]) -> str:
        """Create MCP session for user."""
        client_info = {
            "name": f"user-{user_id}",
            "version": "1.0.0"
        }
        
        session_id = self.host.create_session(client_info, server_configs)
        self.sessions[user_id] = session_id
        
        return session_id
    
    def route_user_request(self, user_id: str, message: Dict) -> Dict:
        """Route user request through MCP session."""
        session_id = self.sessions.get(user_id)
        if not session_id:
            raise ValueError(f"No session for user: {user_id}")
        
        return self.host.route_message(session_id, message)