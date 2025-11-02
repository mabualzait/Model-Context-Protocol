# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.7 Advanced Architectural Patterns

class EventDrivenMCPServer:
    """MCP server with event-driven architecture."""
    
    def __init__(self):
        self.event_handlers: Dict[str, List[callable]] = {}
        self.subscriptions: Dict[str, List[str]] = {}  # resource_uri -> [client_ids]
    
    def subscribe_to_resource(self, client_id: str, resource_uri: str):
        """Subscribe client to resource updates."""
        if resource_uri not in self.subscriptions:
            self.subscriptions[resource_uri] = []
        
        self.subscriptions[resource_uri].append(client_id)
    
    def notify_resource_change(self, resource_uri: str):
        """Notify subscribers of resource change."""
        subscribers = self.subscriptions.get(resource_uri, [])
        
        for client_id in subscribers:
            self._send_notification(client_id, {
                "method": "notifications/resources/updated",
                "params": {
                    "uri": resource_uri
                }
            })