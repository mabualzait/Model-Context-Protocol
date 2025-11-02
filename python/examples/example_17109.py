# 📖 Chapter: Chapter 14: MCP and Enterprise Integration
# 📖 Section: 14.1 Connecting to Enterprise Systems

import psycopg2
from psycopg2 import pool
from typing import Dict, List, Optional
import json
from datetime import datetime

class EnterpriseDatabaseMCP:
    """MCP server for enterprise database integration."""
    
    def __init__(self, db_config: Dict):
        self.db_config = db_config
        self.connection_pool = self._create_connection_pool()
        self.query_cache: Dict[str, Dict] = {}
        self.cache_ttl = 300  # 5 minutes
    
    def _create_connection_pool(self):
        """Create database connection pool."""
        return psycopg2.pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=20,
            host=self.db_config['host'],
            port=self.db_config.get('port', 5432),
            database=self.db_config['database'],
            user=self.db_config['user'],
            password=self.db_config['password']
        )
    
    def list_resources(self) -> List[Dict]:
        """List database tables and views as resources."""
        resources = []
        
        # Get connection from pool
        conn = self.connection_pool.getconn()
        try:
            cursor = conn.cursor()
            
            # Get tables
            cursor.execute("""
                SELECT table_name, table_type
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            
            for table_name, table_type in cursor.fetchall():
                resources.append({
                    "uri": f"db://table/{table_name}",
                    "name": table_name,
                    "description": f"Database {table_type}: {table_name}",
                    "mimeType": "application/json"
                })
            
            cursor.close()
        finally:
            self.connection_pool.putconn(conn)
        
        return resources
    
    def read_resource(self, uri: str, filters: Optional[Dict] = None) -> str:
        """Read database table as resource with optional filters."""
        if not uri.startswith("db://table/"):
            raise ValueError(f"Invalid resource URI: {uri}")
        
        table_name = uri.replace("db://table/", "")
        
        # Validate table name (prevent SQL injection)
        if not self._is_valid_table_name(table_name):
            raise ValueError(f"Invalid table name: {table_name}")
        
        # Build query with filters
        query = f"SELECT * FROM {table_name}"
        params = []
        
        if filters:
            where_clauses = []
            for key, value in filters.items():
                if self._is_valid_column_name(key):
                    where_clauses.append(f"{key} = %s")
                    params.append(value)
            
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
        
        # Add limit
        query += " LIMIT 1000"
        
        # Check cache
        cache_key = f"{uri}:{json.dumps(filters or {})}"
        if cache_key in self.query_cache:
            cached = self.query_cache[cache_key]
            if datetime.now().timestamp() - cached['timestamp'] < self.cache_ttl:
                return cached['data']
        
        # Execute query
        conn = self.connection_pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            # Get column names
            column_names = [desc[0] for desc in cursor.description]
            
            # Fetch results
            rows = cursor.fetchall()
            results = [dict(zip(column_names, row)) for row in rows]
            
            # Cache result
            self.query_cache[cache_key] = {
                'data': json.dumps(results),
                'timestamp': datetime.now().timestamp()
            }
            
            cursor.close()
            return json.dumps(results)
        finally:
            self.connection_pool.putconn(conn)
    
    def _is_valid_table_name(self, name: str) -> bool:
        """Validate table name to prevent SQL injection."""
        # Allow alphanumeric and underscores only
        return name.replace('_', '').isalnum()
    
    def _is_valid_column_name(self, name: str) -> bool:
        """Validate column name to prevent SQL injection."""
        return name.replace('_', '').isalnum()
    
    def list_tools(self) -> List[Dict]:
        """List database query tools."""
        return [
            {
                "name": "query_database",
                "description": "Execute SQL query on enterprise database",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL query (SELECT only)"
                        },
                        "table": {
                            "type": "string",
                            "description": "Table name"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Filter criteria"
                        }
                    },
                    "required": ["table"]
                }
            },
            {
                "name": "execute_stored_procedure",
                "description": "Execute stored procedure",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "procedure_name": {
                            "type": "string",
                            "description": "Stored procedure name"
                        },
                        "parameters": {
                            "type": "object",
                            "description": "Procedure parameters"
                        }
                    },
                    "required": ["procedure_name"]
                }
            }
        ]
    
    def call_tool(self, name: str, arguments: Dict) -> Dict:
        """Execute database tool."""
        if name == "query_database":
            return self._query_database(arguments)
        elif name == "execute_stored_procedure":
            return self._execute_stored_procedure(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    def _query_database(self, arguments: Dict) -> Dict:
        """Execute database query tool."""
        table = arguments.get("table")
        filters = arguments.get("filters")
        
        uri = f"db://table/{table}"
        data = self.read_resource(uri, filters)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": data
                }
            ]
        }
    
    def _execute_stored_procedure(self, arguments: Dict) -> Dict:
        """Execute stored procedure tool."""
        procedure_name = arguments.get("procedure_name")
        parameters = arguments.get("parameters", {})
        
        if not self._is_valid_table_name(procedure_name):
            raise ValueError(f"Invalid procedure name: {procedure_name}")
        
        conn = self.connection_pool.getconn()
        try:
            cursor = conn.cursor()
            
            # Build call
            param_placeholders = ", ".join(["%s"] * len(parameters))
            query = f"CALL {procedure_name}({param_placeholders})"
            
            cursor.execute(query, list(parameters.values()))
            
            if cursor.description:
                column_names = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                results = [dict(zip(column_names, row)) for row in rows]
            else:
                results = {"status": "executed"}
            
            conn.commit()
            cursor.close()
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(results)
                    }
                ]
            }
        except Exception as e:
            conn.rollback()
            raise
        finally:
            self.connection_pool.putconn(conn)