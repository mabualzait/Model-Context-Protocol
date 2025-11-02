# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.7 Advanced Client Patterns

from functools import lru_cache
from typing import Optional
import hashlib
import json

class CachedMCPClient(MCPClient):
    """MCP client with caching capabilities."""
    
    def __init__(self, endpoint: str, transport: str = "stdio", cache_ttl: int = 300):
        super().__init__(endpoint, transport)
        
        self.cache_ttl = cache_ttl
        self.resource_cache: Dict[str, Tuple[Any, float]] = {}
        self.tool_cache: Dict[str, Tuple[Any, float]] = {}
        self.cache_enabled = True
    
    def _cache_key(self, prefix: str, **kwargs) -> str:
        """Generate cache key."""
        key_data = json.dumps(kwargs, sort_keys=True)
        key_hash = hashlib.sha256(key_data.encode()).hexdigest()
        return f"{prefix}:{key_hash}"
    
    def _get_cached(self, cache_key: str, cache_dict: Dict) -> Optional[Any]:
        """Get cached value if not expired."""
        if not self.cache_enabled:
            return None
        
        if cache_key in cache_dict:
            value, timestamp = cache_dict[cache_key]
            
            if time.time() - timestamp < self.cache_ttl:
                return value
            else:
                # Expired, remove from cache
                del cache_dict[cache_key]
        
        return None
    
    def _set_cached(self, cache_key: str, value: Any, cache_dict: Dict):
        """Set cached value."""
        if self.cache_enabled:
            cache_dict[cache_key] = (value, time.time())
    
    def read_resource_cached(self, uri: str) -> str:
        """Read resource with caching."""
        cache_key = self._cache_key("resource", uri=uri)
        
        # Check cache
        cached_value = self._get_cached(cache_key, self.resource_cache)
        if cached_value is not None:
            return cached_value
        
        # Fetch from server
        content = self.read_resource(uri)
        
        # Cache result
        self._set_cached(cache_key, content, self.resource_cache)
        
        return content
    
    def call_tool_cached(self, tool_name: str, arguments: Dict, cacheable: bool = False) -> Dict:
        """Call tool with optional caching."""
        if cacheable:
            cache_key = self._cache_key("tool", name=tool_name, args=arguments)
            
            # Check cache
            cached_value = self._get_cached(cache_key, self.tool_cache)
            if cached_value is not None:
                return cached_value
        
        # Call tool
        result = self.call_tool(tool_name, arguments)
        
        # Cache result if cacheable
        if cacheable:
            cache_key = self._cache_key("tool", name=tool_name, args=arguments)
            self._set_cached(cache_key, result, self.tool_cache)
        
        return result
    
    def invalidate_cache(self, pattern: Optional[str] = None):
        """Invalidate cache entries."""
        if pattern:
            # Invalidate matching entries
            keys_to_remove = [
                key for key in list(self.resource_cache.keys()) + list(self.tool_cache.keys())
                if pattern in key
            ]
            
            for key in keys_to_remove:
                self.resource_cache.pop(key, None)
                self.tool_cache.pop(key, None)
        else:
            # Clear all cache
            self.resource_cache.clear()
            self.tool_cache.clear()