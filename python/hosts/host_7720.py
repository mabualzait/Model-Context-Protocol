# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.4 Resource Pooling and Optimization

class OptimizedMCPHost(MCPHost):
    def __init__(self):
        super().__init__()
        self.connection_pools: Dict[str, ServerConnectionPool] = {}
    
    def get_or_create_pool(self, server_config: Dict) -> ServerConnectionPool:
        """Get or create connection pool for server"""
        server_key = self._get_server_key(server_config)
        
        if server_key not in self.connection_pools:
            pool = ServerConnectionPool(server_config, pool_size=10)
            self.connection_pools[server_key] = pool
        
        return self.connection_pools[server_key]
    
    def _get_server_key(self, server_config: Dict) -> str:
        """Generate unique key for server config"""
        key_parts = [
            server_config.get("transport", "stdio"),
            server_config.get("command") or server_config.get("url", ""),
        ]
        key_string = "|".join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()