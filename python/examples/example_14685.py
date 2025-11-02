# 📖 Chapter: Chapter 11: Monitoring and Observability
# 📖 Section: 11.2 Metrics and Monitoring

import time
from typing import Dict, List
from collections import defaultdict
from threading import Lock

class MetricsCollector:
    """Collect metrics from MCP systems."""
    
    def __init__(self):
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self.lock = Lock()
    
    def increment_counter(self, name: str, value: int = 1, labels: Dict = None):
        """Increment counter metric."""
        key = self._build_key(name, labels)
        with self.lock:
            self.counters[key] += value
    
    def set_gauge(self, name: str, value: float, labels: Dict = None):
        """Set gauge metric."""
        key = self._build_key(name, labels)
        with self.lock:
            self.gauges[key] = value
    
    def record_histogram(self, name: str, value: float, labels: Dict = None):
        """Record histogram value."""
        key = self._build_key(name, labels)
        with self.lock:
            self.histograms[key].append(value)
            # Keep only recent values
            if len(self.histograms[key]) > 1000:
                self.histograms[key] = self.histograms[key][-1000:]
    
    def get_metrics(self) -> Dict:
        """Get all metrics."""
        with self.lock:
            return {
                "counters": dict(self.counters),
                "gauges": dict(self.gauges),
                "histograms": {
                    key: {
                        "count": len(values),
                        "sum": sum(values),
                        "avg": sum(values) / len(values) if values else 0,
                        "min": min(values) if values else 0,
                        "max": max(values) if values else 0
                    }
                    for key, values in self.histograms.items()
                }
            }
    
    def _build_key(self, name: str, labels: Dict = None) -> str:
        """Build metric key with labels."""
        if not labels:
            return name
        
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

class MCPMetrics:
    """MCP-specific metrics."""
    
    def __init__(self, collector: MetricsCollector):
        self.collector = collector
    
    def record_request(self, method: str, duration_ms: float, success: bool):
        """Record request metrics."""
        self.collector.increment_counter(
            "mcp_requests_total",
            labels={"method": method, "status": "success" if success else "error"}
        )
        self.collector.record_histogram(
            "mcp_request_duration_ms",
            duration_ms,
            labels={"method": method}
        )
    
    def record_resource_access(self, resource_type: str, action: str):
        """Record resource access metrics."""
        self.collector.increment_counter(
            "mcp_resource_access_total",
            labels={"type": resource_type, "action": action}
        )
    
    def record_tool_execution(self, tool_name: str, duration_ms: float, success: bool):
        """Record tool execution metrics."""
        self.collector.increment_counter(
            "mcp_tool_executions_total",
            labels={"tool": tool_name, "status": "success" if success else "error"}
        )
        self.collector.record_histogram(
            "mcp_tool_duration_ms",
            duration_ms,
            labels={"tool": tool_name}
        )
    
    def record_session_count(self, count: int):
        """Record active session count."""
        self.collector.set_gauge("mcp_sessions_active", count)