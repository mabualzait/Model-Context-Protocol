# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.3 Session Isolation and Security

import hashlib
import secrets

class SecureMCPHost(MCPHost):
    def __init__(self, security_config: Dict):
        super().__init__()
        self.security_config = security_config
        self.authentication_tokens: Dict[str, str] = {}
    
    def authenticate_client(self, client_id: str, credentials: Dict) -> Optional[str]:
        """Authenticate client and return session token"""
        # Validate credentials
        if not self._validate_credentials(client_id, credentials):
            return None
        
        # Generate session token
        token = secrets.token_urlsafe(32)
        self.authentication_tokens[token] = {
            "client_id": client_id,
            "expires_at": time.time() + self.security_config.get("session_timeout", 3600)
        }
        
        return token
    
    def validate_session_token(self, token: str) -> bool:
        """Validate session token"""
        token_data = self.authentication_tokens.get(token)
        if not token_data:
            return False
        
        # Check expiration
        if token_data["expires_at"] < time.time():
            del self.authentication_tokens[token]
            return False
        
        return True
    
    def create_authenticated_session(self, token: str, server_config: Dict) -> str:
        """Create session with authentication"""
        if not self.validate_session_token(token):
            raise ValueError("Invalid or expired token")
        
        token_data = self.authentication_tokens[token]
        client_info = {
            "name": token_data["client_id"],
            "version": "1.0.0"
        }
        
        return self.create_session(client_info, server_config)
    
    def _validate_credentials(self, client_id: str, credentials: Dict) -> bool:
        """Validate client credentials"""
        # Implementation depends on authentication method
        # Example: API key, OAuth, etc.
        expected_api_key = self.security_config.get("api_keys", {}).get(client_id)
        provided_api_key = credentials.get("api_key")
        
        return expected_api_key and expected_api_key == provided_api_key