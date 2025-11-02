# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.7 Advanced Client Patterns

from typing import Callable, Dict, List

class EventDrivenMCPClient(MCPClient):
    """MCP client with event-driven capabilities."""
    
    def __init__(self, endpoint: str, transport: str = "stdio"):
        super().__init__(endpoint, transport)
        
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.subscriptions: Dict[str, bool] = {}
    
    def on(self, event: str, handler: Callable):
        """Register event handler."""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    def emit(self, event: str, *args, **kwargs):
        """Emit event to handlers."""
        handlers = self.event_handlers.get(event, [])
        for handler in handlers:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in event handler for {event}: {e}")
    
    def subscribe_resource(self, uri: str):
        """Subscribe to resource with event handling."""
        super().subscribe_resource(uri)
        self.subscriptions[uri] = True
        self.emit("resource_subscribed", uri)
    
    def handle_resource_update(self, notification: Dict):
        """Handle resource update with events."""
        uri = notification["params"].get("uri")
        
        self.emit("resource_update_started", uri)
        
        try:
            updated_content = self.read_resource(uri)
            self.emit("resource_updated", uri, updated_content)
        except Exception as e:
            self.emit("resource_update_failed", uri, e)