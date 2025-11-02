# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.2 Identity Fragmentation and Mitigation

class ContextAwareMCPHost:
    """MCP host that propagates identity context."""
    
    def route_message(self, session_id: str, message: Dict) -> Dict:
        """Route message with identity context."""
        # Get user identity from session
        user_id = self.get_user_id(session_id)
        
        # Add identity context to message
        message["params"] = message.get("params", {})
        message["params"]["_identity"] = {
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": time.time()
        }
        
        # Route to server
        return super().route_message(session_id, message)
    
    def validate_identity_context(self, message: Dict) -> bool:
        """Validate identity context in message."""
        identity = message.get("params", {}).get("_identity")
        if not identity:
            return False
        
        # Validate user_id
        user_id = identity.get("user_id")
        if not user_id or not self.user_exists(user_id):
            return False
        
        # Validate session_id matches user_id
        session_id = identity.get("session_id")
        expected_user_id = self.get_user_id(session_id)
        
        return user_id == expected_user_id