# 📖 Chapter: Chapter 9: Advanced MCP Patterns
# 📖 Section: 9.3 Performance Optimization and Caching

from functools import lru_cache
from datetime import datetime, timedelta
import hashlib
import json

class CachedMCPClient:
    """MCP client with intelligent caching."""
    
    def __init__(self, client: MCPClient, cache_ttl: int = 3600):
        self.client = client
        self.cache: Dict[str, Dict] = {}
        self.cache_ttl = cache_ttl  # Time to live in seconds
    
    def _generate_cache_key(self, operation: str, params: Dict) -> str:
        """Generate cache key from operation and parameters."""
        key_data = {
            'operation': operation,
            'params': params
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if cache entry is still valid."""
        expiry_time = cache_entry['timestamp'] + timedelta(seconds=self.cache_ttl)
        return datetime.now() < expiry_time
    
    def read_resource_cached(self, uri: str, force_refresh: bool = False) -> str:
        """Read resource with caching."""
        cache_key = self._generate_cache_key('read_resource', {'uri': uri})
        
        if not force_refresh and cache_key in self.cache:
            entry = self.cache[cache_key]
            if self._is_cache_valid(entry):
                return entry['data']
        
        # Fetch from server
        data = self.client.read_resource(uri)
        
        # Cache result
        self.cache[cache_key] = {
            'data': data,
            'timestamp': datetime.now()
        }
        
        return data
    
    def call_tool_cached(self, tool_name: str, arguments: Dict,
                        force_refresh: bool = False) -> Dict:
        """Call tool with caching (only for read-only operations)."""
        # Only cache if tool is marked as cacheable
        if not self._is_tool_cacheable(tool_name):
            return self.client.call_tool(tool_name, arguments)
        
        cache_key = self._generate_cache_key('call_tool', {
            'tool': tool_name,
            'args': arguments
        })
        
        if not force_refresh and cache_key in self.cache:
            entry = self.cache[cache_key]
            if self._is_cache_valid(entry):
                return entry['data']
        
        # Call tool
        result = self.client.call_tool(tool_name, arguments)
        
        # Cache result
        self.cache[cache_key] = {
            'data': result,
            'timestamp': datetime.now()
        }
        
        return result
    
    def _is_tool_cacheable(self, tool_name: str) -> bool:
        """Check if tool results are cacheable."""
        # Tools that modify state should not be cached
        non_cacheable_keywords = ['write', 'delete', 'update', 'create', 'modify']
        tool_lower = tool_name.lower()
        
        return not any(keyword in tool_lower for keyword in non_cacheable_keywords)
    
    def invalidate_cache(self, pattern: str = None):
        """Invalidate cache entries matching pattern."""
        if pattern is None:
            self.cache.clear()
            return
        
        keys_to_remove = [
            key for key in self.cache.keys()
            if pattern in key
        ]
        
        for key in keys_to_remove:
            del self.cache[key]