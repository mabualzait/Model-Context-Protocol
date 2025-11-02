# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.7 Monitoring and Observability in Hosts

class MonitoredMCPHost(MCPHost):
    """Host with comprehensive monitoring."""
    
    def __init__(self):
        super().__init__()
        self.metrics = {
            "sessions_created": 0,
            "sessions_destroyed": 0,
            "requests_total": 0,
            "requests_by_method": {},
            "requests_by_status": {"success": 0, "error": 0},
            "avg_request_latency": 0,
            "server_connections": 0,
            "errors": []
        }
        self.start_time = time.time()
    
    def create_session(self, client_info: Dict, server_config: Dict) -> str:
        """Create session with metrics."""
        start_time = time.time()
        
        try:
            session_id = super().create_session(client_info, server_config)
            
            self.metrics["sessions_created"] += 1
            self.metrics["server_connections"] += len(server_config) if isinstance(server_config, list) else 1
            
            duration = time.time() - start_time
            logger.info(f"Session created: {session_id} in {duration:.3f}s")
            
            return session_id
        except Exception as e:
            self.metrics["errors"].append({
                "timestamp": time.time(),
                "type": "session_creation_error",
                "error": str(e)
            })
            raise
    
    def route_message(self, session_id: str, message: Dict) -> Optional[Dict]:
        """Route message with metrics."""
        method = message.get("method", "unknown")
        start_time = time.time()
        
        try:
            response = super().route_message(session_id, message)
            
            duration = time.time() - start_time
            
            # Update metrics
            self.metrics["requests_total"] += 1
            self.metrics["requests_by_method"][method] = (
                self.metrics["requests_by_method"].get(method, 0) + 1
            )
            self.metrics["requests_by_status"]["success"] += 1
            
            # Update average latency
            total_requests = self.metrics["requests_total"]
            current_avg = self.metrics["avg_request_latency"]
            self.metrics["avg_request_latency"] = (
                (current_avg * (total_requests - 1) + duration * 1000) /
                total_requests
            )
            
            # Log slow requests
            if duration > 1.0:
                logger.warning(f"Slow request: {method} took {duration:.3f}s")
            
            return response
        except Exception as e:
            duration = time.time() - start_time
            
            # Update error metrics
            self.metrics["requests_total"] += 1
            self.metrics["requests_by_method"][method] = (
                self.metrics["requests_by_method"].get(method, 0) + 1
            )
            self.metrics["requests_by_status"]["error"] += 1
            self.metrics["errors"].append({
                "timestamp": time.time(),
                "type": "request_error",
                "method": method,
                "error": str(e),
                "duration": duration
            })
            
            logger.error(f"Request failed: {method} - {e}")
            raise
    
    def get_metrics(self) -> Dict:
        """Get host metrics."""
        uptime = time.time() - self.start_time
        
        return {
            **self.metrics,
            "uptime_seconds": uptime,
            "requests_per_second": (
                self.metrics["requests_total"] / uptime
                if uptime > 0 else 0
            ),
            "error_rate": (
                self.metrics["requests_by_status"]["error"] /
                max(self.metrics["requests_total"], 1)
            ),
            "active_sessions": len(self.sessions)
        }
    
    def get_health_report(self) -> Dict:
        """Get health report."""
        error_rate = (
            self.metrics["requests_by_status"]["error"] /
            max(self.metrics["requests_total"], 1)
        )
        
        health_status = "healthy"
        if error_rate > 0.1:  # More than 10% error rate
            health_status = "degraded"
        if error_rate > 0.5:  # More than 50% error rate
            health_status = "unhealthy"
        
        return {
            "status": health_status,
            "uptime_seconds": time.time() - self.start_time,
            "active_sessions": len(self.sessions),
            "error_rate": error_rate,
            "avg_latency_ms": self.metrics["avg_request_latency"],
            "requests_per_second": (
                self.metrics["requests_total"] /
                (time.time() - self.start_time)
                if (time.time() - self.start_time) > 0 else 0
            )
        }