# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.4 Complete Server Implementation

#!/usr/bin/env python3
"""Complete MCP server example."""

import sys
import json
from pathlib import Path
from typing import Any, Dict, List

from mcp import Server, Resource, Tool, Prompt
from my_mcp_server.resources import FileSystemResources
from my_mcp_server.tools import FileSystemTools

class MyMCPServer:
    """Complete MCP server implementation."""
    
    def __init__(self, name: str = "my-server", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.protocol_version = "2024-11-05"
        
        # Initialize components
        self.fs_resources = FileSystemResources("/tmp/mcp-workspace")
        self.fs_tools = FileSystemTools("/tmp/mcp-workspace")
        
        # Initialize server
        self.server = Server(
            name=self.name,
            version=self.version,
            protocol_version=self.protocol_version
        )
        
        # Register handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register MCP handlers."""
        # Resources
        self.server.on_list_resources = self._list_resources
        self.server.on_read_resource = self._read_resource
        
        # Tools
        self.server.on_list_tools = self._list_tools
        self.server.on_call_tool = self._call_tool
        
        # Prompts
        self.server.on_list_prompts = self._list_prompts
        self.server.on_get_prompt = self._get_prompt
    
    def _list_resources(self) -> List[Resource]:
        """List available resources."""
        return self.fs_resources.list_resources()
    
    def _read_resource(self, uri: str) -> str:
        """Read resource content."""
        return self.fs_resources.read_resource(uri)
    
    def _list_tools(self) -> List[Tool]:
        """List available tools."""
        return self.fs_tools.list_tools()
    
    def _call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool."""
        return self.fs_tools.call_tool(name, arguments)
    
    def _list_prompts(self) -> List[Prompt]:
        """List available prompts."""
        return []
    
    def _get_prompt(self, name: str, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get prompt messages."""
        raise ValueError(f"Prompt not found: {name}")
    
    def run(self):
        """Run the server."""
        self.server.run()

if __name__ == "__main__":
    server = MyMCPServer()
    server.run()