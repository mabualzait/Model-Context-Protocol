# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.1 Authentication and Authorization

import requests
from typing import Optional

class OAuthAuth:
    """OAuth 2.0 authentication for MCP."""
    
    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.validated_tokens: Dict[str, Dict] = {}
    
    def validate_access_token(self, access_token: str) -> Optional[Dict]:
        """Validate OAuth access token."""
        # Check cache
        if access_token in self.validated_tokens:
            return self.validated_tokens[access_token]
        
        # Validate with OAuth provider
        try:
            response = requests.get(
                f"{self.token_url}/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=5
            )
            response.raise_for_status()
            
            user_info = response.json()
            self.validated_tokens[access_token] = user_info
            
            return user_info
        except Exception as e:
            return None