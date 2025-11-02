# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.7 Testing MCP Clients

import subprocess
import time

class TestMCPClientIntegration(unittest.TestCase):
    def setUp(self):
        # Start test server
        self.server_process = subprocess.Popen(
            ["python", "test-server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(0.5)  # Wait for server to start
        
        self.client = MCPClient(["python", "test-server.py"])
        self.client.process = self.server_process
    
    def tearDown(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
    
    def test_full_workflow(self):
        """Test complete client workflow"""
        # Connect
        init_result = self.client.connect()
        self.assertIsNotNone(init_result)
        
        # List resources
        resources = self.client.list_resources()
        self.assertIsInstance(resources, list)
        
        # List tools
        tools = self.client.list_tools()
        self.assertIsInstance(tools, list)
        
        # Disconnect
        self.client.disconnect()