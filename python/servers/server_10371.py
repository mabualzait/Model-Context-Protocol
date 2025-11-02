# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.6 Production Deployment Considerations

from prometheus_client import Counter, Histogram, Gauge, start_http_server

class PrometheusMetrics:
    """Prometheus metrics for MCP server."""
    
    def __init__(self):
        # Request metrics
        self.request_count = Counter(
            'mcp_requests_total',
            'Total number of MCP requests',
            ['method', 'status']
        )
        
        self.request_latency = Histogram(
            'mcp_request_duration_seconds',
            'MCP request latency',
            ['method']
        )
        
        # Resource metrics
        self.resource_reads = Counter(
            'mcp_resource_reads_total',
            'Total resource reads',
            ['uri']
        )
        
        # Tool metrics
        self.tool_calls = Counter(
            'mcp_tool_calls_total',
            'Total tool calls',
            ['tool_name', 'status']
        )
        
        # Connection metrics
        self.active_connections = Gauge(
            'mcp_active_connections',
            'Number of active connections'
        )
    
    def record_request(self, method: str, status: str, duration: float):
        """Record request metrics."""
        self.request_count.labels(method=method, status=status).inc()
        self.request_latency.labels(method=method).observe(duration)
    
    def record_resource_read(self, uri: str):
        """Record resource read."""
        self.resource_reads.labels(uri=uri).inc()
    
    def record_tool_call(self, tool_name: str, status: str):
        """Record tool call."""
        self.tool_calls.labels(tool_name=tool_name, status=status).inc()
    
    def set_active_connections(self, count: int):
        """Update active connections gauge."""
        self.active_connections.set(count)
    
    def start_metrics_server(self, port: int = 9090):
        """Start Prometheus metrics HTTP server."""
        start_http_server(port)
        print(f"Metrics server started on port {port}")