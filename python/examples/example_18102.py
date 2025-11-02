# 📖 Chapter: Chapter 14: MCP and Enterprise Integration
# 📖 Section: 14.4 Scalability and Performance at Scale

class HorizontalScaler:
    """Manage horizontal scaling of MCP servers."""
    
    def __init__(self, min_instances: int = 2, max_instances: int = 10):
        self.min_instances = min_instances
        self.max_instances = max_instances
        self.current_instances: List['MCPServer'] = []
        self.metrics_collector = MetricsCollector()
    
    def should_scale_up(self) -> bool:
        """Determine if should scale up."""
        if len(self.current_instances) >= self.max_instances:
            return False
        
        metrics = self.metrics_collector.get_metrics()
        cpu_usage = metrics.get("cpu_usage", 0)
        request_rate = metrics.get("requests_per_second", 0)
        
        # Scale up if CPU > 70% or request rate > threshold
        return cpu_usage > 70 or request_rate > 100
    
    def should_scale_down(self) -> bool:
        """Determine if should scale down."""
        if len(self.current_instances) <= self.min_instances:
            return False
        
        metrics = self.metrics_collector.get_metrics()
        cpu_usage = metrics.get("cpu_usage", 0)
        request_rate = metrics.get("requests_per_second", 0)
        
        # Scale down if CPU < 30% and request rate < threshold
        return cpu_usage < 30 and request_rate < 20
    
    def scale_up(self):
        """Add new server instance."""
        if len(self.current_instances) < self.max_instances:
            new_server = self._create_server_instance()
            self.current_instances.append(new_server)
            return new_server
        return None
    
    def scale_down(self):
        """Remove server instance."""
        if len(self.current_instances) > self.min_instances:
            removed = self.current_instances.pop()
            self._destroy_server_instance(removed)
            return removed
        return None
    
    def _create_server_instance(self) -> 'MCPServer':
        """Create new server instance."""
        # In production, this would spawn a new process/container
        return MCPServer()
    
    def _destroy_server_instance(self, server: 'MCPServer'):
        """Destroy server instance."""
        # In production, this would terminate the process/container
        server.shutdown()