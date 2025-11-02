# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.6 Production Deployment Considerations

class HealthCheckManager:
    """Health check management for MCP server."""
    
    def __init__(self, server: 'MCPServer'):
        self.server = server
        self.health_status = {
            "status": "healthy",
            "timestamp": time.time(),
            "checks": {}
        }
    
    def perform_health_check(self) -> Dict:
        """Perform comprehensive health check."""
        checks = {}
        
        # Check server status
        checks["server_status"] = self._check_server_status()
        
        # Check resources
        checks["resources"] = self._check_resources()
        
        # Check tools
        checks["tools"] = self._check_tools()
        
        # Check performance
        checks["performance"] = self._check_performance()
        
        # Overall status
        all_healthy = all(
            check.get("status") == "healthy"
            for check in checks.values()
        )
        
        self.health_status = {
            "status": "healthy" if all_healthy else "unhealthy",
            "timestamp": time.time(),
            "checks": checks
        }
        
        return self.health_status
    
    def _check_server_status(self) -> Dict:
        """Check server operational status."""
        return {
            "status": "healthy",
            "uptime": time.time() - self.server.start_time,
            "active_connections": len(self.server.active_sessions)
        }
    
    def _check_resources(self) -> Dict:
        """Check resource availability."""
        try:
            resources = self.server.list_resources()
            return {
                "status": "healthy",
                "resource_count": len(resources),
                "accessible": True
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def _check_tools(self) -> Dict:
        """Check tool availability."""
        try:
            tools = self.server.list_tools()
            return {
                "status": "healthy",
                "tool_count": len(tools),
                "accessible": True
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def _check_performance(self) -> Dict:
        """Check performance metrics."""
        metrics = self.server.get_metrics()
        
        avg_latency = metrics.get("avg_latency_ms", 0)
        error_rate = metrics.get("error_rate", 0)
        
        healthy = avg_latency < 1000 and error_rate < 0.05
        
        return {
            "status": "healthy" if healthy else "degraded",
            "avg_latency_ms": avg_latency,
            "error_rate": error_rate
        }