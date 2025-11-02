# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.3 Resource Discovery and Access

class MCPClient:
    def list_resources(self):
        """List all available resources"""
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "resources/list"
        }
        
        response = self._send_request(request)
        
        if response.get("error"):
            raise ValueError(f"Failed to list resources: {response['error']}")
        
        resources = response["result"].get("resources", [])
        
        # Update session state
        for resource in resources:
            self.session.add_resource(resource)
        
        return resources