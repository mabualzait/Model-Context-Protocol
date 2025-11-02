# 📁 File: python/utils/session_state.py
# 📖 Chapter 2, Section 2.8: Protocol Implementation Deep Dive
# 🔗 GitHub: https://github.com/mabualzait/Model-Context-Protocol/blob/main/python/utils/session_state.py

# MCP Session State Management
import time
from typing import Dict, List, Optional, Any

class MCPSessionState:
    """Manages state for an MCP session."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.protocol_version: Optional[str] = None
        self.client_info: Dict = {}
        self.server_info: Dict = {}
        self.client_capabilities: Dict = {}
        self.server_capabilities: Dict = {}
        self.resource_subscriptions: Dict[str, List[str]] = {}  # uri -> [client_ids]
        self.context: Dict = {}
        self.authentication: Dict = {}
        self.created_at = time.time()
        self.last_activity = time.time()
    
    def initialize(self, protocol_version: str, client_info: Dict, client_capabilities: Dict):
        """Initialize session state."""
        self.protocol_version = protocol_version
        self.client_info = client_info
        self.client_capabilities = client_capabilities
        self.last_activity = time.time()
    
    def set_server_info(self, server_info: Dict, server_capabilities: Dict):
        """Set server information and capabilities."""
        self.server_info = server_info
        self.server_capabilities = server_capabilities
    
    def subscribe_resource(self, uri: str, client_id: str):
        """Subscribe to resource updates."""
        if uri not in self.resource_subscriptions:
            self.resource_subscriptions[uri] = []
        
        if client_id not in self.resource_subscriptions[uri]:
            self.resource_subscriptions[uri].append(client_id)
    
    def unsubscribe_resource(self, uri: str, client_id: str):
        """Unsubscribe from resource updates."""
        if uri in self.resource_subscriptions:
            if client_id in self.resource_subscriptions[uri]:
                self.resource_subscriptions[uri].remove(client_id)
            
            if not self.resource_subscriptions[uri]:
                del self.resource_subscriptions[uri]
    
    def get_resource_subscribers(self, uri: str) -> List[str]:
        """Get list of clients subscribed to resource."""
        return self.resource_subscriptions.get(uri, [])
    
    def update_context(self, key: str, value: Any):
        """Update session context."""
        self.context[key] = value
        self.last_activity = time.time()
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get session context value."""
        return self.context.get(key, default)
    
    def is_expired(self, timeout: int = 3600) -> bool:
        """Check if session has expired."""
        return (time.time() - self.last_activity) > timeout

