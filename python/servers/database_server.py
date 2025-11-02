# 📁 File: python/servers/database_server.py
# 📖 Chapter 1, Section 1.9: Use Case 2 - Enterprise Database Integration
# 🔗 GitHub: https://github.com/mabualzait/Model-Context-Protocol/blob/main/python/servers/database_server.py

# Database MCP Server
import psycopg2
from typing import Dict, List, Optional
from datetime import datetime
import json

# Note: MCPServer, Resource, and Tool classes would be imported from your MCP SDK
# from mcp_sdk import MCPServer, Resource, Tool

class DatabaseMCPServer:
    """MCP server exposing database operations."""
    
    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(connection_string)
        self.server = MCPServer(name="database", version="1.0.0")
        self._register_handlers()
    
    def _list_resources(self) -> List[Resource]:
        """List database tables as resources."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        
        resources = []
        for row in cursor.fetchall():
            table_name = row[0]
            resources.append(Resource(
                uri=f"db://table/{table_name}",
                name=table_name,
                mimeType="application/json",
                description=f"Database table: {table_name}"
            ))
        
        cursor.close()
        return resources
    
    def _read_resource(self, uri: str) -> str:
        """Read table data as resource."""
        if uri.startswith("db://table/"):
            table_name = uri.replace("db://table/", "")
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            data = [dict(zip(columns, row)) for row in rows]
            cursor.close()
            
            return json.dumps(data, indent=2, default=str)
        else:
            raise ValueError(f"Unknown resource URI: {uri}")
    
    def _list_tools(self) -> List[Tool]:
        """List database operations as tools."""
        return [
            Tool(
                name="query",
                description="Execute SQL query",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "sql": {"type": "string"},
                        "params": {"type": "object"}
                    },
                    "required": ["sql"]
                }
            )
        ]
    
    def _call_tool(self, name: str, arguments: Dict) -> Dict:
        """Execute database operation."""
        if name == "query":
            sql = arguments["sql"]
            params = arguments.get("params", {})
            
            cursor = self.conn.cursor()
            try:
                cursor.execute(sql, params)
                
                if sql.strip().upper().startswith("SELECT"):
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    data = [dict(zip(columns, row)) for row in rows]
                    result = {"data": data, "count": len(data)}
                else:
                    self.conn.commit()
                    result = {"affected_rows": cursor.rowcount}
                
                cursor.close()
                return {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2, default=str)}],
                    "isError": False
                }
            except Exception as e:
                self.conn.rollback()
                cursor.close()
                return {
                    "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                    "isError": True
                }
        else:
            raise ValueError(f"Unknown tool: {name}")

