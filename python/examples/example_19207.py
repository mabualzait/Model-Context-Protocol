# 📖 Chapter: Chapter 15: The Future of MCP
# 📖 Section: 15.5 Innovation Opportunities

class AdvancedMCPMonitor:
    """Advanced monitoring for MCP systems."""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.trace_collector = TraceCollector()
        self.alert_manager = AlertManager()
    
    def create_dashboard(self) -> Dict:
        """Create monitoring dashboard."""
        return {
            "metrics": self.metrics_collector.get_metrics(),
            "traces": self.trace_collector.get_recent_traces(),
            "alerts": self.alert_manager.get_active_alerts(),
            "health": self._assess_system_health()
        }
    
    def _assess_system_health(self) -> Dict:
        """Assess overall system health."""
        metrics = self.metrics_collector.get_metrics()
        
        health_score = 100
        
        # Deduct points for issues
        error_rate = metrics.get("error_rate", 0)
        if error_rate > 0.05:  # >5% error rate
            health_score -= 20
        
        avg_latency = metrics.get("avg_latency_ms", 0)
        if avg_latency > 1000:  # >1 second
            health_score -= 15
        
        return {
            "score": max(health_score, 0),
            "status": "healthy" if health_score >= 80 else "degraded"
        }