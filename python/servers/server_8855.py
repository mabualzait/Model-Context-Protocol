# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.1 Getting Started: Project Setup

#!/usr/bin/env python3
"""A simple MCP server example."""

import sys
import json
from typing import Any, Dict, List
from mcp import Server, Resource, Tool, Prompt

class SimpleMCPServer:
    """Simple MCP server implementation."""
    
    def __init__(self, name: str = "simple-server", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.protocol_version = "2024-11-05"
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
        return []
    
    def _read_resource(self, uri: str) -> str:
        """Read resource content."""
        raise ValueError(f"Resource not found: {uri}")
    
    def _list_tools(self) -> List[Tool]:
        """List available tools."""
        return []
    
    def _call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool."""
        raise ValueError(f"Tool not found: {name}")
    
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
    server = SimpleMCPServer()
    server.run()