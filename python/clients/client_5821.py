# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.3 Resource Discovery and Access

class MCPClient:
    def subscribe_resource(self, uri):
        """Subscribe to resource updates"""
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "resources/subscribe",
            "params": {
                "uri": uri
            }
        }
        
        response = self._send_request(request)
        
        if response.get("error"):
            raise ValueError(f"Failed to subscribe: {response['error']}")
        
        self.session.subscriptions[uri] = True
        return response["result"]
    
    def handle_resource_update(self, notification):
        """Handle resource update notification"""
        uri = notification["params"].get("uri")
        if uri in self.session.subscriptions:
            # Resource changed, re-read if needed
            updated_content = self.read_resource(uri)
            self.on_resource_updated(uri, updated_content)
    
    def on_resource_updated(self, uri, content):
        """Callback for resource updates"""
        # Override in subclass or provide callback
        pass