# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.2 Implementing Resources

import sqlite3
from typing import List, Dict, Any
from mcp import Resource

class DatabaseResources:
    """Database resource implementation."""
    
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.conn = sqlite3.connect(database_path)
        self.conn.row_factory = sqlite3.Row
    
    def list_resources(self) -> List[Resource]:
        """List tables as resources."""
        resources = []
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        
        for row in cursor.fetchall():
            table_name = row[0]
            uri = f"db://table/{table_name}"
            resources.append(Resource(
                uri=uri,
                name=table_name,
                mimeType="application/json",
                description=f"Table: {table_name}"
            ))
        
        return resources
    
    def read_resource(self, uri: str) -> str:
        """Read table data."""
        if not uri.startswith("db://table/"):
            raise ValueError(f"Invalid URI: {uri}")
        
        table_name = uri.replace("db://table/", "")
        
        # Security: validate table name (prevent SQL injection)
        if not table_name.replace("_", "").replace("-", "").isalnum():
            raise ValueError(f"Invalid table name: {table_name}")
        
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
        
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        
        import json
        return json.dumps(data, indent=2)