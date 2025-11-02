# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.6 Complete Client Implementation Example

import json
import subprocess
import sys
from typing import Dict, Any, List, Optional
from functools import wraps
import time

class MCPClient:
    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.process = None
        self.request_id = 0
        self.session = MCPSession()
    
    def connect(self):
        """Connect to server"""
        self.process = subprocess.Popen(
            self.server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Initialize
        init_response = self._send_request({
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "python-mcp-client",
                    "version": "1.0.0"
                }
            }
        })
        
        self.session.update_capabilities(init_response["result"].get("capabilities", {}))
        self.session.server_info = init_response["result"].get("serverInfo", {})
        
        # Send initialized notification
        self._send_notification({
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        })
        
        return init_response["result"]
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """List available resources"""
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "resources/list"
        })
        
        resources = response["result"].get("resources", [])
        for resource in resources:
            self.session.add_resource(resource)
        
        return resources
    
    def read_resource(self, uri: str) -> str:
        """Read resource content"""
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "resources/read",
            "params": {"uri": uri}
        })
        
        contents = response["result"].get("contents", [])
        if contents:
            return contents[0].get("text", "")
        return ""
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools"""
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "tools/list"
        })
        
        tools = response["result"].get("tools", [])
        for tool in tools:
            self.session.add_tool(tool)
        
        return tools
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call tool"""
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        })
        
        result = response["result"]
        if result.get("isError"):
            raise RuntimeError(f"Tool error: {result.get('content', [{}])[0].get('text', 'Unknown')}")
        
        return result.get("content", [])
    
    def disconnect(self):
        """Disconnect from server"""
        if self.process:
            self._send_request({
                "jsonrpc": "2.0",
                "id": self._get_next_id(),
                "method": "shutdown"
            })
            self.process.terminate()
            self.process.wait()
            self.process = None
    
    def _get_next_id(self) -> int:
        """Get next request ID"""
        self.request_id += 1
        return self.request_id
    
    def _send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send request and wait for response"""
        request_str = json.dumps(request) + "\n"
        self.process.stdin.write(request_str)
        self.process.stdin.flush()
        
        response_line = self.process.stdout.readline()
        response = json.loads(response_line.strip())
        
        if response.get("error"):
            raise MCPError(f"Request failed: {response['error']}")
        
        return response
    
    def _send_notification(self, notification: Dict[str, Any]):
        """Send notification"""
        notification_str = json.dumps(notification) + "\n"
        self.process.stdin.write(notification_str)
        self.process.stdin.flush()

class MCPSession:
    def __init__(self):
        self.server_capabilities = {}
        self.server_info = {}
        self.resources = {}
        self.tools = {}
        self.prompts = {}
    
    def update_capabilities(self, capabilities):
        self.server_capabilities = capabilities
    
    def add_resource(self, resource):
        self.resources[resource["uri"]] = resource
    
    def add_tool(self, tool):
        self.tools[tool["name"]] = tool
    
    def add_prompt(self, prompt):
        self.prompts[prompt["name"]] = prompt

# Example usage
if __name__ == "__main__":
    client = MCPClient(["python", "filesystem-server.py"])
    client.connect()
    
    # List resources
    resources = client.list_resources()
    print(f"Found {len(resources)} resources")
    
    # Read a resource
    if resources:
        content = client.read_resource(resources[0]["uri"])
        print(f"Resource content: {content[:100]}...")
    
    # List tools
    tools = client.list_tools()
    print(f"Found {len(tools)} tools")
    
    # Call a tool
    if tools:
        tool_name = tools[0]["name"]
        result = client.call_tool(tool_name, {})
        print(f"Tool result: {result}")
    
    client.disconnect()