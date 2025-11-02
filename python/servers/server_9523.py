# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.5 Testing and Debugging

import subprocess
import json
import time
from my_mcp_server.server import MyMCPServer

class TestMCPServerIntegration(unittest.TestCase):
    """Integration tests with MCP client."""
    
    def setUp(self):
        """Start server process."""
        self.server_process = subprocess.Popen(
            ["python", "-m", "my_mcp_server.server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(1)  # Wait for server to start
    
    def tearDown(self):
        """Stop server process."""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
    
    def test_initialize(self):
        """Test server initialization."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = self._send_request(request)
        
        self.assertIn("result", response)
        self.assertEqual(response["result"]["protocolVersion"], "2024-11-05")
    
    def test_list_tools(self):
        """Test listing tools."""
        # Initialize first
        self._initialize()
        
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        response = self._send_request(request)
        
        self.assertIn("result", response)
        self.assertIn("tools", response["result"])
    
    def _initialize(self):
        """Initialize server."""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1.0.0"}
            }
        }
        self._send_request(request)
        
        # Send initialized notification
        notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        self._send_notification(notification)
    
    def _send_request(self, request):
        """Send request to server."""
        request_str = json.dumps(request) + "\n"
        self.server_process.stdin.write(request_str)
        self.server_process.stdin.flush()
        
        response_line = self.server_process.stdout.readline()
        return json.loads(response_line.strip())
    
    def _send_notification(self, notification):
        """Send notification to server."""
        notification_str = json.dumps(notification) + "\n"
        self.server_process.stdin.write(notification_str)
        self.server_process.stdin.flush()