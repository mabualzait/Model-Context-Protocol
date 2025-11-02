# 📖 Chapter: Chapter 15: The Future of MCP
# 📖 Section: 15.5 Innovation Opportunities

class MCPMarketplace:
    """Marketplace for MCP servers."""
    
    def __init__(self):
        self.server_registry: Dict[str, Dict] = {}
        self.ratings: Dict[str, Dict] = {}
        self.download_counts: Dict[str, int] = {}
    
    def register_server(self, server_metadata: Dict):
        """Register MCP server in marketplace."""
        server_id = server_metadata['id']
        
        self.server_registry[server_id] = {
            **server_metadata,
            "registered_at": time.time(),
            "downloads": 0,
            "rating": 0.0
        }
    
    def search_servers(self, query: str, filters: Dict = None) -> List[Dict]:
        """Search for MCP servers."""
        results = []
        
        query_lower = query.lower()
        
        for server_id, server in self.server_registry.items():
            # Simple text matching (in production, use better search)
            if (query_lower in server.get('name', '').lower() or
                query_lower in server.get('description', '').lower()):
                
                # Apply filters
                if filters:
                    if not self._matches_filters(server, filters):
                        continue
                
                results.append(server)
        
        # Sort by relevance, rating, or downloads
        results.sort(key=lambda x: x.get('rating', 0), reverse=True)
        
        return results
    
    def _matches_filters(self, server: Dict, filters: Dict) -> bool:
        """Check if server matches filters."""
        for key, value in filters.items():
            if server.get(key) != value:
                return False
        return True
    
    def rate_server(self, server_id: str, rating: float, review: str):
        """Rate and review MCP server."""
        if server_id not in self.server_registry:
            raise ValueError(f"Server {server_id} not found")
        
        if server_id not in self.ratings:
            self.ratings[server_id] = []
        
        self.ratings[server_id].append({
            "rating": rating,
            "review": review,
            "timestamp": time.time()
        })
        
        # Update average rating
        ratings = self.ratings[server_id]
        avg_rating = sum(r['rating'] for r in ratings) / len(ratings)
        self.server_registry[server_id]['rating'] = avg_rating