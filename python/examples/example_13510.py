# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.1 Authentication and Authorization

import hashlib
import hmac

class APIKeyAuth:
    """API key-based authentication."""
    
    def __init__(self, api_keys: Dict[str, str]):
        # api_keys format: {key_id: secret_key}
        self.api_keys = api_keys
    
    def validate_api_key(self, key_id: str, signature: str, message: str) -> bool:
        """Validate API key signature."""
        secret_key = self.api_keys.get(key_id)
        if not secret_key:
            return False
        
        expected_signature = hmac.new(
            secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def create_signature(self, key_id: str, message: str) -> str:
        """Create signature for message."""
        secret_key = self.api_keys.get(key_id)
        if not secret_key:
            raise ValueError(f"Unknown key ID: {key_id}")
        
        return hmac.new(
            secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()