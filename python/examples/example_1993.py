# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.8 Performance and Scalability Considerations

class MCPConnectionPool:
    """Pool of MCP server connections."""
    
    def __init__(self, server_endpoint: str, max_connections: int = 10):
        self.server_endpoint = server_endpoint
        self.max_connections = max_connections
        self.pool: Queue = Queue(maxsize=max_connections)
        self.active_count = 0
    
    def get_connection(self) -> 'MCPClient':
        """Get connection from pool."""
        if not self.pool.empty():
            return self.pool.get()
        
        # Create new connection if under limit
        if self.active_count < self.max_connections:
            conn = MCPClient(self.server_endpoint)
            conn.connect()
            self.active_count += 1
            return conn
        
        # Wait for available connection
        return self.pool.get(block=True, timeout=5)
    
    def return_connection(self, conn: 'MCPClient'):
        """Return connection to pool."""
        self.pool.put(conn)