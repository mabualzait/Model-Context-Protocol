# 📖 Chapter: Appendices
# 📖 Section: E.3 Performance Tuning Guide

# Implement resource caching
from functools import lru_cache

@lru_cache(maxsize=1000)
def read_resource_cached(uri: str):
    return client.read_resource(uri)

# Cache tool results (for read-only tools)
cache_ttl = 3600  # 1 hour
cached_tool_results = {}