# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.7 Testing MCP Clients

import unittest
from unittest.mock import Mock, patch
import json

class TestMCPClient(unittest.TestCase):
    def setUp(self):
        self.client = MCPClient(["mock-server"])
    
    def test_list_resources(self):
        """Test resource listing"""
        with patch.object(self.client, '_send_request') as mock_request:
            mock_request.return_value = {
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "resources": [
                        {"uri": "file:///test.txt", "name": "test.txt"}
                    ]
                }
            }
            
            resources = self.client.list_resources()
            self.assertEqual(len(resources), 1)
            self.assertEqual(resources[0]["uri"], "file:///test.txt")
    
    def test_read_resource(self):
        """Test resource reading"""
        with patch.object(self.client, '_send_request') as mock_request:
            mock_request.return_value = {
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "contents": [
                        {"uri": "file:///test.txt", "text": "Test content"}
                    ]
                }
            }
            
            content = self.client.read_resource("file:///test.txt")
            self.assertEqual(content, "Test content")
    
    def test_call_tool(self):
        """Test tool invocation"""
        with patch.object(self.client, '_send_request') as mock_request:
            mock_request.return_value = {
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "content": [{"type": "text", "text": "Success"}],
                    "isError": False
                }
            }
            
            result = self.client.call_tool("test_tool", {"arg": "value"})
            self.assertIsNotNone(result)
            self.assertFalse(result.get("isError", True))

if __name__ == "__main__":
    unittest.main()