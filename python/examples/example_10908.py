# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.1 Adding MCP Support to Existing Applications

from mcp_server import MCPServer

class MyServerApplication:
    """Application exposing capabilities via MCP."""
    
    def __init__(self):
        self.app_data = {}  # Application state
        self.mcp_server = MCPServer("my-app-server", "1.0.0")
        self._register_mcp_handlers()
    
    def _register_mcp_handlers(self):
        """Register MCP handlers."""
        self.mcp_server.on_list_resources = self._list_resources
        self.mcp_server.on_read_resource = self._read_resource
        self.mcp_server.on_list_tools = self._list_tools
        self.mcp_server.on_call_tool = self._call_tool
    
    def _list_resources(self) -> List[Resource]:
        """List application resources."""
        return [
            Resource(
                uri=f"app://data/{key}",
                name=key,
                mimeType="application/json",
                description=f"Application data: {key}"
            )
            for key in self.app_data.keys()
        ]
    
    def _read_resource(self, uri: str) -> str:
        """Read application resource."""
        if not uri.startswith("app://data/"):
            raise ValueError(f"Invalid URI: {uri}")
        
        key = uri.replace("app://data/", "")
        data = self.app_data.get(key)
        
        import json
        return json.dumps(data)
    
    def _list_tools(self) -> List[Tool]:
        """List application tools."""
        return [
            Tool(
                name="get_data",
                description="Get application data",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "key": {"type": "string"}
                    },
                    "required": ["key"]
                }
            ),
            Tool(
                name="set_data",
                description="Set application data",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "key": {"type": "string"},
                        "value": {"type": "object"}
                    },
                    "required": ["key", "value"]
                }
            )
        ]
    
    def _call_tool(self, name: str, arguments: Dict) -> Dict:
        """Call application tool."""
        if name == "get_data":
            key = arguments["key"]
            data = self.app_data.get(key)
            return {
                "content": [{"type": "text", "text": json.dumps(data)}],
                "isError": False
            }
        elif name == "set_data":
            key = arguments["key"]
            value = arguments["value"]
            self.app_data[key] = value
            return {
                "content": [{"type": "text", "text": f"Set {key}"}],
                "isError": False
            }
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    def run_mcp_server(self):
        """Run MCP server."""
        self.mcp_server.run()