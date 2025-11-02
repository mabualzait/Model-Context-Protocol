# 📖 Chapter: Chapter 11: Monitoring and Observability
# 📖 Section: 11.2 Metrics and Monitoring

from prometheus_client import Counter, Histogram, Gauge, generate_latest

class PrometheusMetrics:
    """Prometheus metrics for MCP."""
    
    def __init__(self):
        # Counters
        self.requests_total = Counter(
            'mcp_requests_total',
            'Total MCP requests',
            ['method', 'status']
        )
        
        self.resource_access_total = Counter(
            'mcp_resource_access_total',
            'Total resource access',
            ['type', 'action']
        )
        
        self.tool_executions_total = Counter(
            'mcp_tool_executions_total',
            'Total tool executions',
            ['tool', 'status']
        )
        
        # Histograms
        self.request_duration = Histogram(
            'mcp_request_duration_seconds',
            'Request duration in seconds',
            ['method'],
            buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
        )
        
        # Gauges
        self.active_sessions = Gauge(
            'mcp_sessions_active',
            'Number of active sessions'
        )
    
    def record_request(self, method: str, duration: float, success: bool):
        """Record request metrics."""
        self.requests_total.labels(
            method=method,
            status="success" if success else "error"
        ).inc()
        
        self.request_duration.labels(method=method).observe(duration)
    
    def get_metrics(self) -> bytes:
        """Get metrics in Prometheus format."""
        return generate_latest()