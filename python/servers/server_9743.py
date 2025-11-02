# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.4 Advanced Testing Strategies

import pytest
from mcp_client import MCPClient
from my_mcp_server.server import SimpleMCPServer
import subprocess
import time

class TestMCPIntegration:
    """Integration tests for MCP server."""
    
    @pytest.fixture
    def server_process(self):
        """Start MCP server process."""
        process = subprocess.Popen(
            ["python", "-m", "my_mcp_server.server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(0.5)
        
        yield process
        
        # Cleanup
        process.terminate()
        process.wait()
    
    def test_server_initialization(self, server_process):
        """Test server initialization."""
        client = MCPClient("stdio", server_process)
        client.connect()
        
        assert client.protocol_version == "2024-11-05"
        assert client.server_info["name"] == "simple-server"
    
    def test_resource_listing(self, server_process):
        """Test resource listing."""
        client = MCPClient("stdio", server_process)
        client.connect()
        
        resources = client.list_resources()
        assert isinstance(resources, list)
    
    def test_tool_execution(self, server_process):
        """Test tool execution."""
        client = MCPClient("stdio", server_process)
        client.connect()
        
        result = client.call_tool("read_file", {"path": "test.txt"})
        assert "content" in result