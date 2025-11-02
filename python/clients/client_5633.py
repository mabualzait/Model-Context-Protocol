# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.2 Connection Management and Session Handling

import requests
import sseclient
import json

class MCPHTTPClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.sse_client = None
        self.session_id = None
    
    def connect(self):
        """Connect to server via HTTP/SSE"""
        # Initialize session
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "example-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = requests.post(
            f"{self.server_url}/messages",
            json=init_request,
            headers={"Content-Type": "application/json"}
        )
        
        response_data = response.json()
        
        if response_data.get("error"):
            raise ConnectionError(f"Initialization failed: {response_data['error']}")
        
        # Establish SSE connection for server-to-client messages
        sse_response = requests.get(
            f"{self.server_url}/sse",
            headers={"Accept": "text/event-stream"},
            stream=True
        )
        
        self.sse_client = sseclient.SSEClient(sse_response)
        
        # Send initialized notification
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        self._send_notification(initialized_notification)
        
        self.session_id = response_data["result"].get("serverInfo", {}).get("name")
        return response_data["result"]
    
    def _send_request(self, request):
        """Send request via HTTP"""
        response = requests.post(
            f"{self.server_url}/messages",
            json=request,
            headers={"Content-Type": "application/json"}
        )
        return response.json()
    
    def _send_notification(self, notification):
        """Send notification via HTTP"""
        requests.post(
            f"{self.server_url}/messages",
            json=notification,
            headers={"Content-Type": "application/json"}
        )
    
    def disconnect(self):
        """Disconnect from server"""
        if self.sse_client:
            self.sse_client.close()
            self.sse_client = None
        
        shutdown_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "shutdown"
        }
        self._send_request(shutdown_request)