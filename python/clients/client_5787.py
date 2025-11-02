# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.3 Resource Discovery and Access

class MCPClient:
    def read_resource(self, uri):
        """Read resource content"""
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "resources/read",
            "params": {
                "uri": uri
            }
        }
        
        response = self._send_request(request)
        
        if response.get("error"):
            raise ValueError(f"Failed to read resource: {response['error']}")
        
        contents = response["result"].get("contents", [])
        
        # Process contents
        for content in contents:
            if content.get("mimeType") == "text/plain":
                return content.get("text")
            elif content.get("mimeType") == "application/json":
                return json.loads(content.get("text"))
            else:
                return content.get("text")