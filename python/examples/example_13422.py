# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.1 Authentication and Authorization

import secrets
import time
from typing import Dict, Optional
from functools import wraps

class TokenAuth:
    """Token-based authentication for MCP."""
    
    def __init__(self):
        self.tokens: Dict[str, Dict] = {}
        self.token_expiry = 3600  # 1 hour
    
    def generate_token(self, user_id: str, permissions: List[str]) -> str:
        """Generate authentication token."""
        token = secrets.token_urlsafe(32)
        self.tokens[token] = {
            "user_id": user_id,
            "permissions": permissions,
            "created_at": time.time(),
            "expires_at": time.time() + self.token_expiry
        }
        return token
    
    def validate_token(self, token: str) -> Optional[Dict]:
        """Validate token and return user info."""
        token_data = self.tokens.get(token)
        
        if not token_data:
            return None
        
        # Check expiration
        if time.time() > token_data["expires_at"]:
            del self.tokens[token]
            return None
        
        return token_data
    
    def revoke_token(self, token: str):
        """Revoke token."""
        self.tokens.pop(token, None)

class AuthenticatedMCPServer:
    """MCP server with authentication."""
    
    def __init__(self):
        self.auth = TokenAuth()
        self.sessions: Dict[str, Dict] = {}
    
    def authenticate(self, token: str) -> str:
        """Authenticate client and create session."""
        token_data = self.auth.validate_token(token)
        
        if not token_data:
            raise ValueError("Invalid or expired token")
        
        session_id = secrets.token_urlsafe(16)
        self.sessions[session_id] = {
            "user_id": token_data["user_id"],
            "permissions": token_data["permissions"],
            "created_at": time.time()
        }
        
        return session_id
    
    def authorize(self, session_id: str, resource: str, action: str) -> bool:
        """Check if session has permission for action."""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        permissions = session["permissions"]
        
        # Check permissions
        if "admin" in permissions:
            return True
        
        if action == "read":
            return "read" in permissions or f"read:{resource}" in permissions
        
        if action == "write":
            return "write" in permissions or f"write:{resource}" in permissions
        
        return False