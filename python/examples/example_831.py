# 📖 Chapter: Chapter 1: Introduction to Model Context Protocol
# 📖 Section: 1.9 Detailed Use Cases and Implementation Examples

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
                mimeType="application/json"
            ))
        return resources
    
    def _read_resource(self, uri: str) -> str:
        """Read table data as resource."""
        table_name = uri.replace("db://table/", "")
        
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
        
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        data = [dict(zip(columns, row)) for row in rows]
        return json.dumps(data, indent=2)
    
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
                        "params": {"type": "array"}
                    },
                    "required": ["sql"]
                }
            ),
            Tool(
                name="insert",
                description="Insert data into table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table": {"type": "string"},
                        "data": {"type": "object"}
                    },
                    "required": ["table", "data"]
                }
            )
        ]
    
    def _call_tool(self, name: str, arguments: Dict) -> Dict:
        """Execute database operation."""
        if name == "query":
            cursor = self.conn.cursor()
            cursor.execute(arguments["sql"], arguments.get("params", []))
            
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                data = [dict(zip(columns, row)) for row in rows]
                return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}
            else:
                self.conn.commit()
                return {"content": [{"type": "text", "text": "Query executed successfully"}]}
        
        elif name == "insert":
            table = arguments["table"]
            data = arguments["data"]
            
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            
            cursor = self.conn.cursor()
            cursor.execute(
                f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                list(data.values())
            )
            self.conn.commit()
            
            return {"content": [{"type": "text", "text": "Insert successful"}]}
        else:
            raise ValueError(f"Unknown tool: {name}")