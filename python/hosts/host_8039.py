# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.5 Advanced Host Patterns

class LoadBalancedMCPHost(MCPHost):
    """Host with load balancing across multiple server instances."""
    
    def __init__(self):
        super().__init__()
        self.server_pools: Dict[str, ServerConnectionPool] = {}
        self.load_balancers: Dict[str, LoadBalancer] = {}
        self.server_metrics: Dict[str, Dict] = {}
    
    def register_server_pool(self, server_id: str, server_configs: List[Dict]):
        """Register pool of server instances."""
        pool = ServerConnectionPool(
            server_configs[0],  # Use first config as template
            pool_size=len(server_configs) * 2
        )
        
        # Create connections for all server instances
        for config in server_configs:
            connection = pool._create_connection()
            pool.active_connections.add(connection)
        
        self.server_pools[server_id] = pool
        
        # Create load balancer
        self.load_balancers[server_id] = LoadBalancer(strategy="round_robin")
        self.server_metrics[server_id] = {
            "requests": 0,
            "errors": 0,
            "avg_latency": 0
        }
    
    def route_request(self, session_id: str, request: Dict) -> Dict:
        """Route request with load balancing."""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        # Determine target server
        method = request.get("method", "")
        server_id = self._select_server(session, method)
        
        # Get connection from pool
        pool = self.server_pools[server_id]
        connection = pool.get_connection()
        
        start_time = time.time()
        try:
            # Route request
            response = connection.send_request(request)
            
            # Record metrics
            duration = time.time() - start_time
            self._record_success(server_id, duration)
            
            return response
        except Exception as e:
            # Record error
            duration = time.time() - start_time
            self._record_error(server_id, duration, e)
            
            # Return connection to pool if healthy, otherwise discard
            if connection.is_healthy():
                pool.return_connection(connection)
            else:
                pool.active_connections.discard(connection)
            
            raise
        finally:
            pool.return_connection(connection)
    
    def _select_server(self, session: MCPSession, method: str) -> str:
        """Select server for request using load balancer."""
        # Determine which servers can handle this request
        available_servers = session.get_available_servers_for_method(method)
        
        if not available_servers:
            raise ValueError(f"No server available for method: {method}")
        
        # Use load balancer to select server
        if len(available_servers) == 1:
            return available_servers[0]
        
        # Select based on metrics
        best_server = min(available_servers, key=lambda s: self._get_server_score(s))
        return best_server
    
    def _get_server_score(self, server_id: str) -> float:
        """Calculate server score for load balancing."""
        metrics = self.server_metrics[server_id]
        
        # Lower score is better
        error_rate = metrics["errors"] / max(metrics["requests"], 1)
        latency_score = metrics["avg_latency"] / 1000  # Convert to seconds
        
        # Weighted score
        score = (error_rate * 10) + latency_score
        return score
    
    def _record_success(self, server_id: str, duration: float):
        """Record successful request."""
        metrics = self.server_metrics[server_id]
        metrics["requests"] += 1
        
        # Update average latency
        metrics["avg_latency"] = (
            (metrics["avg_latency"] * (metrics["requests"] - 1) + duration * 1000) /
            metrics["requests"]
        )
    
    def _record_error(self, server_id: str, duration: float, error: Exception):
        """Record failed request."""
        metrics = self.server_metrics[server_id]
        metrics["requests"] += 1
        metrics["errors"] += 1