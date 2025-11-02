# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.9 Best Practices for Client Design

class ManagedConnection:
    """Managed connection with health checks."""
    
    def __init__(self, client: 'MCPClient'):
        self.client = client
        self.last_health_check = time.time()
        self.health_check_interval = 30
    
    def is_healthy(self) -> bool:
        """Check if connection is healthy."""
        try:
            # Simple health check: try to list tools
            self.client.list_tools()
            self.last_health_check = time.time()
            return True
        except Exception:
            return False
    
    def ensure_healthy(self):
        """Ensure connection is healthy, reconnect if needed."""
        if time.time() - self.last_health_check > self.health_check_interval:
            if not self.is_healthy():
                self.client.disconnect()
                self.client.connect()