# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.8 Performance and Scalability Considerations

class CachedMCPClient:
    """MCP client with intelligent caching."""
    
    def __init__(self, client: 'MCPClient'):
        self.client = client
        self.cache: Dict[str, CacheEntry] = {}
        self.cache_ttl = 300  # 5 minutes default
    
    def read_resource_cached(self, uri: str) -> str:
        """Read resource with caching."""
        cache_key = f"resource:{uri}"
        
        # Check cache
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if not entry.is_expired():
                return entry.data
        
        # Fetch from server
        data = self.client.read_resource(uri)
        
        # Cache result
        self.cache[cache_key] = CacheEntry(
            data=data,
            ttl=self.cache_ttl
        )
        
        return data
    
    def invalidate_cache(self, pattern: str):
        """Invalidate cache entries matching pattern."""
        keys_to_remove = [
            key for key in self.cache.keys()
            if pattern in key
        ]
        
        for key in keys_to_remove:
            del self.cache[key]

class CacheEntry:
    """Cache entry with TTL."""
    
    def __init__(self, data: Any, ttl: int):
        self.data = data
        self.created_at = time.time()
        self.ttl = ttl
    
    def is_expired(self) -> bool:
        """Check if cache entry is expired."""
        return time.time() - self.created_at > self.ttl