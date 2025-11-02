# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.8 Performance and Scalability Considerations

class LoadBalancedMCPHost:
    """Host with load balancing across server instances."""
    
    def __init__(self, server_endpoints: List[str]):
        self.servers: List['MCPClient'] = [
            MCPClient(endpoint) for endpoint in server_endpoints
        ]
        self.current_index = 0
        self.server_metrics: Dict[int, Dict] = {}
    
    def route_request(self, request: Dict) -> Dict:
        """Route request using round-robin load balancing."""
        server = self._select_server()
        
        start_time = time.time()
        try:
            result = server.handle_request(request)
            self._record_success(server, time.time() - start_time)
            return result
        except Exception as e:
            self._record_error(server, e)
            raise
    
    def _select_server(self) -> 'MCPClient':
        """Select server using round-robin."""
        server = self.servers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server
    
    def _record_success(self, server: 'MCPClient', duration: float):
        """Record successful request."""
        server_id = id(server)
        if server_id not in self.server_metrics:
            self.server_metrics[server_id] = {
                "requests": 0,
                "errors": 0,
                "avg_duration": 0
            }
        
        metrics = self.server_metrics[server_id]
        metrics["requests"] += 1
        metrics["avg_duration"] = (
            (metrics["avg_duration"] * (metrics["requests"] - 1) + duration) /
            metrics["requests"]
        )