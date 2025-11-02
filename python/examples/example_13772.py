# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.2 Identity Fragmentation and Mitigation

import jwt
import json

class UnifiedIdentityToken:
    """Unified identity token for all MCP servers."""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def create_token(self, user_id: str, permissions: List[str], metadata: Dict) -> str:
        """Create unified identity token."""
        payload = {
            "user_id": user_id,
            "permissions": permissions,
            "metadata": metadata,
            "iat": time.time(),
            "exp": time.time() + 3600
        }
        
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    def validate_token(self, token: str) -> Optional[Dict]:
        """Validate unified identity token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def get_user_id(self, token: str) -> Optional[str]:
        """Extract user ID from token."""
        payload = self.validate_token(token)
        return payload.get("user_id") if payload else None