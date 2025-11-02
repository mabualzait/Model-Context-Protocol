# 📖 Chapter: Chapter 3: MCP in the Ecosystem
# 📖 Section: 3.9 Building Ecosystem-Aware Applications

# Example: Database MCP Server
import json
from mcp_server import MCPServer

class DatabaseMCPServer(MCPServer):
    def __init__(self, database_config):
        super().__init__()
        self.db = connect_database(database_config)
        
    def initialize(self, request):
        """Initialize server with client capabilities"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "serverInfo": {
                "name": "database-server",
                "version": "1.0.0"
            }
        }
    
    def list_tools(self):
        """List available tools"""
        return {
            "tools": [
                {
                    "name": "query",
                    "description": "Execute SQL query",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "sql": {"type": "string"},
                            "params": {"type": "object"}
                        },
                        "required": ["sql"]
                    }
                }
            ]
        }
    
    def call_tool(self, name, arguments):
        """Execute tool"""
        if name == "query":
            sql = arguments.get("sql")
            params = arguments.get("params", {})
            result = self.db.execute(sql, params)
            return {
                "content": [
                    {"type": "text", "text": json.dumps(result)}
                ],
                "isError": False
            }
        else:
            raise ValueError(f"Unknown tool: {name}")

# Usage: Works with any MCP client
server = DatabaseMCPServer({"host": "localhost", "database": "mydb"})
server.run()