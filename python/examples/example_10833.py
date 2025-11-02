# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.1 Adding MCP Support to Existing Applications

from mcp_client import MCPClient
from typing import Dict, List, Optional

class MyApplication:
    """Application with MCP integration."""
    
    def __init__(self):
        self.mcp_clients: Dict[str, MCPClient] = {}
        self.mcp_servers = []  # List of configured servers
    
    def initialize_mcp(self, server_configs: List[Dict]):
        """Initialize MCP servers."""
        for config in server_configs:
            server_id = config.get("id", config.get("name"))
            client = MCPClient(config["command"])
            client.connect()
            self.mcp_clients[server_id] = client
    
    def use_mcp_resource(self, server_id: str, uri: str) -> str:
        """Use MCP resource in application."""
        if server_id not in self.mcp_clients:
            raise ValueError(f"Server not found: {server_id}")
        
        client = self.mcp_clients[server_id]
        return client.read_resource(uri)
    
    def use_mcp_tool(self, server_id: str, tool_name: str, arguments: Dict) -> Dict:
        """Use MCP tool in application."""
        if server_id not in self.mcp_clients:
            raise ValueError(f"Server not found: {server_id}")
        
        client = self.mcp_clients[server_id]
        return client.call_tool(tool_name, arguments)