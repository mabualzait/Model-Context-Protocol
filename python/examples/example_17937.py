# 📖 Chapter: Chapter 14: MCP and Enterprise Integration
# 📖 Section: 14.4 Scalability and Performance at Scale

from enum import Enum

class LoadBalancingStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED = "weighted"
    CONSISTENT_HASH = "consistent_hash"

class AdvancedLoadBalancer:
    """Advanced load balancer for MCP servers."""
    
    def __init__(self, strategy: LoadBalancingStrategy):
        self.strategy = strategy
        self.servers: List[Dict] = []
        self.server_metrics: Dict[str, Dict] = {}
        self.current_index = 0
    
    def add_server(self, server_id: str, server: 'MCPServer', 
                   weight: int = 1):
        """Add server to load balancer."""
        self.servers.append({
            "id": server_id,
            "server": server,
            "weight": weight,
            "connections": 0,
            "requests": 0
        })
        
        self.server_metrics[server_id] = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_response_time": 0,
            "current_connections": 0
        }
    
    def select_server(self, request: Dict) -> 'MCPServer':
        """Select server based on load balancing strategy."""
        if not self.servers:
            raise ValueError("No servers available")
        
        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._round_robin()
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._least_connections()
        elif self.strategy == LoadBalancingStrategy.WEIGHTED:
            return self._weighted_round_robin()
        elif self.strategy == LoadBalancingStrategy.CONSISTENT_HASH:
            return self._consistent_hash(request)
        else:
            return self.servers[0]["server"]
    
    def _round_robin(self) -> 'MCPServer':
        """Round-robin server selection."""
        server = self.servers[self.current_index % len(self.servers)]
        self.current_index += 1
        return server["server"]
    
    def _least_connections(self) -> 'MCPServer':
        """Select server with least connections."""
        server = min(self.servers, key=lambda s: s["connections"])
        server["connections"] += 1
        return server["server"]
    
    def _weighted_round_robin(self) -> 'MCPServer':
        """Weighted round-robin selection."""
        total_weight = sum(s["weight"] for s in self.servers)
        target = self.current_index % total_weight
        
        cumulative = 0
        for server in self.servers:
            cumulative += server["weight"]
            if target < cumulative:
                self.current_index += 1
                return server["server"]
        
        return self.servers[0]["server"]
    
    def _consistent_hash(self, request: Dict) -> 'MCPServer':
        """Consistent hashing for request routing."""
        request_key = json.dumps(request, sort_keys=True)
        hash_value = hash(request_key)
        
        server_index = hash_value % len(self.servers)
        return self.servers[server_index]["server"]
    
    def record_request(self, server_id: str, success: bool, 
                      duration_ms: float):
        """Record request metrics."""
        if server_id in self.server_metrics:
            metrics = self.server_metrics[server_id]
            metrics["total_requests"] += 1
            
            if success:
                metrics["successful_requests"] += 1
            else:
                metrics["failed_requests"] += 1
            
            # Update average response time
            total = metrics["total_requests"]
            metrics["avg_response_time"] = (
                (metrics["avg_response_time"] * (total - 1) + duration_ms) / total
            )

class ScalableMCPServer:
    """Scalable MCP server with load balancing and caching."""
    
    def __init__(self, load_balancer: AdvancedLoadBalancer):
        self.load_balancer = load_balancer
        self.cache = LRUCache(maxsize=10000)
        self.request_id = 0
    
    def handle_request(self, request: Dict) -> Dict:
        """Handle request with load balancing and caching."""
        import hashlib
        
        # Check cache
        cache_key = self._generate_cache_key(request)
        cached_response = self.cache.get(cache_key)
        if cached_response:
            return cached_response
        
        # Route to server
        start_time = time.time()
        server = self.load_balancer.select_server(request)
        
        try:
            response = server.handle_request(request)
            duration_ms = (time.time() - start_time) * 1000
            
            # Record success
            server_id = self._get_server_id(server)
            self.load_balancer.record_request(server_id, True, duration_ms)
            
            # Cache response (only for read operations)
            if request.get("method") in ["resources/list", "resources/read"]:
                self.cache[cache_key] = response
            
            return response
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            # Record failure
            server_id = self._get_server_id(server)
            self.load_balancer.record_request(server_id, False, duration_ms)
            raise
    
    def _generate_cache_key(self, request: Dict) -> str:
        """Generate cache key from request."""
        key_data = {
            "method": request.get("method"),
            "params": request.get("params", {})
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    def _get_server_id(self, server: 'MCPServer') -> str:
        """Get server ID from server instance."""
        # In production, maintain a mapping
        return "server_1"