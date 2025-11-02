# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.2 Connection Management and Session Handling

import subprocess
import json
import sys

class MCPClient:
    def __init__(self, server_command):
        self.server_command = server_command
        self.process = None
        self.session_id = None
    
    def connect(self):
        """Connect to server via stdio"""
        self.process = subprocess.Popen(
            self.server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
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
        
        response = self._send_request(init_request)
        
        if response.get("error"):
            raise ConnectionError(f"Initialization failed: {response['error']}")
        
        # Send initialized notification
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        self._send_notification(initialized_notification)
        
        self.session_id = response["result"].get("serverInfo", {}).get("name")
        return response["result"]
    
    def _send_request(self, request):
        """Send request and wait for response"""
        request_str = json.dumps(request) + "\n"
        self.process.stdin.write(request_str)
        self.process.stdin.flush()
        
        response_line = self.process.stdout.readline()
        return json.loads(response_line.strip())
    
    def _send_notification(self, notification):
        """Send notification (no response expected)"""
        notification_str = json.dumps(notification) + "\n"
        self.process.stdin.write(notification_str)
        self.process.stdin.flush()
    
    def disconnect(self):
        """Disconnect from server"""
        if self.process:
            shutdown_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "shutdown"
            }
            self._send_request(shutdown_request)
            self.process.terminate()
            self.process.wait()
            self.process = None