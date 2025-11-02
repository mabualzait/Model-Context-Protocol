# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.6 Complete Server Implementation Example

import json
import sys
from typing import Dict, Any, List

class MCPServer:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.protocol_version = "2024-11-05"
        self.state = {}
        self.resources = {}
        self.tools = {}
        self.prompts = {}
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                result = self.initialize(params)
            elif method == "resources/list":
                result = self.list_resources()
            elif method == "resources/read":
                result = self.read_resource(params.get("uri"))
            elif method == "tools/list":
                result = self.list_tools()
            elif method == "tools/call":
                result = self.call_tool(
                    params.get("name"),
                    params.get("arguments", {})
                )
            elif method == "prompts/list":
                result = self.list_prompts()
            elif method == "prompts/get":
                result = self.get_prompt(
                    params.get("name"),
                    params.get("arguments", {})
                )
            elif method == "shutdown":
                result = self.shutdown()
            else:
                raise ValueError(f"Unknown method: {method}")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e)
                }
            }
    
    def initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize server"""
        self.state["client"] = params.get("clientInfo", {})
        self.state["client_capabilities"] = params.get("capabilities", {})
        
        return {
            "protocolVersion": self.protocol_version,
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "serverInfo": {
                "name": self.name,
                "version": self.version
            }
        }
    
    def list_resources(self) -> Dict[str, Any]:
        """List resources"""
        return {"resources": list(self.resources.values())}
    
    def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read resource"""
        if uri not in self.resources:
            raise ValueError(f"Resource not found: {uri}")
        # Implementation depends on resource type
        return {"contents": []}
    
    def list_tools(self) -> Dict[str, Any]:
        """List tools"""
        return {"tools": list(self.tools.values())}
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call tool"""
        if name not in self.tools:
            raise ValueError(f"Tool not found: {name}")
        # Implementation depends on tool
        return {
            "content": [{"type": "text", "text": "Tool executed"}],
            "isError": False
        }
    
    def list_prompts(self) -> Dict[str, Any]:
        """List prompts"""
        return {"prompts": list(self.prompts.values())}
    
    def get_prompt(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get prompt"""
        if name not in self.prompts:
            raise ValueError(f"Prompt not found: {name}")
        # Implementation depends on prompt
        return {"messages": []}
    
    def shutdown(self) -> Dict[str, Any]:
        """Shutdown server"""
        self.cleanup()
        return {}
    
    def cleanup(self):
        """Clean up server state"""
        self.state.clear()
        self.resources.clear()
        self.tools.clear()
        self.prompts.clear()
    
    def run_stdio(self):
        """Run server with stdio transport"""
        for line in sys.stdin:
            request = json.loads(line.strip())
            response = self.handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()

# Example usage
if __name__ == "__main__":
    server = MCPServer("example-server", "1.0.0")
    server.run_stdio()