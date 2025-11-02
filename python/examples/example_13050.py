# 📖 Chapter: Chapter 9: Advanced MCP Patterns
# 📖 Section: 9.3 Performance Optimization and Caching

from queue import Queue
from threading import Lock

class MCPConnectionPool:
    """Pool of MCP client connections for reuse."""
    
    def __init__(self, endpoint: str, transport: str, max_connections: int = 10):
        self.endpoint = endpoint
        self.transport = transport
        self.max_connections = max_connections
        self.pool: Queue = Queue(maxsize=max_connections)
        self.active_connections = 0
        self.lock = Lock()
    
    def get_connection(self) -> MCPClient:
        """Get connection from pool or create new one."""
        if not self.pool.empty():
            return self.pool.get()
        
        with self.lock:
            if self.active_connections < self.max_connections:
                client = MCPClient(self.endpoint, self.transport)
                client.connect()
                self.active_connections += 1
                return client
        
        # Wait for available connection
        return self.pool.get()
    
    def return_connection(self, client: MCPClient):
        """Return connection to pool."""
        # Reset connection state if needed
        self.pool.put(client)
    
    def close_all(self):
        """Close all connections in pool."""
        while not self.pool.empty():
            client = self.pool.get()
            try:
                client.disconnect()
            except:
                pass
        
        self.active_connections = 0