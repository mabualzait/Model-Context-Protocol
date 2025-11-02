# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.2 Identity Fragmentation and Mitigation

class CentralizedIdentity:
    """Centralized identity management."""
    
    def __init__(self):
        self.user_identities: Dict[str, Dict] = {}
        self.session_mapping: Dict[str, str] = {}  # session_id -> user_id
    
    def create_unified_session(self, user_id: str, servers: List[str]) -> str:
        """Create unified session across all servers."""
        session_id = secrets.token_urlsafe(32)
        
        # Store user identity
        self.user_identities[user_id] = {
            "session_id": session_id,
            "servers": servers,
            "created_at": time.time()
        }
        
        # Map session to user
        self.session_mapping[session_id] = user_id
        
        # Authenticate to all servers with same identity
        for server in servers:
            self._authenticate_to_server(user_id, server, session_id)
        
        return session_id
    
    def get_user_id(self, session_id: str) -> Optional[str]:
        """Get user ID from session."""
        return self.session_mapping.get(session_id)
    
    def _authenticate_to_server(self, user_id: str, server: str, session_id: str):
        """Authenticate to server with unified identity."""
        # Use same identity token across all servers
        identity_token = self._generate_unified_token(user_id, session_id)
        # Authenticate to server...