# 📖 Chapter: Chapter 11: Monitoring and Observability
# 📖 Section: 11.5 Error Tracking and Alerting

import traceback
from typing import Dict, List
from datetime import datetime, timedelta

class ErrorTracker:
    """Track and analyze errors."""
    
    def __init__(self):
        self.errors: List[Dict] = []
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.max_errors = 10000
    
    def record_error(self, error: Exception, context: Dict = None):
        """Record error with context."""
        error_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        
        self.errors.append(error_entry)
        
        # Track error counts
        error_key = f"{error_entry['error_type']}:{error_entry['error_message']}"
        self.error_counts[error_key] += 1
        
        # Limit error history
        if len(self.errors) > self.max_errors:
            self.errors = self.errors[-self.max_errors:]
    
    def get_error_summary(self, hours: int = 24) -> Dict:
        """Get error summary for period."""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        recent_errors = [
            e for e in self.errors
            if datetime.fromisoformat(e["timestamp"]) > cutoff
        ]
        
        return {
            "total_errors": len(recent_errors),
            "error_types": {
                error["error_type"]: sum(
                    1 for e in recent_errors if e["error_type"] == error["error_type"]
                )
                for error in recent_errors
            },
            "most_common": sorted(
                self.error_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }

# --- Additional code from line 15158 ---
# 📖 Chapter: Chapter 11: Monitoring and Observability
# 📖 Section: 11.5 Error Tracking and Alerting

from typing import Callable, List

class AlertManager:
    """Manage alerts and notifications."""
    
    def __init__(self):
        self.alert_rules: List[Callable] = []
        self.alert_handlers: List[Callable] = []
        self.alert_history: List[Dict] = []
    
    def add_alert_rule(self, rule: Callable[[Dict], bool]):
        """Add alert rule."""
        self.alert_rules.append(rule)
    
    def add_alert_handler(self, handler: Callable[[Dict], None]):
        """Add alert handler (e.g., send email, Slack, etc.)."""
        self.alert_handlers.append(handler)
    
    def check_alerts(self, metrics: Dict):
        """Check metrics against alert rules."""
        for rule in self.alert_rules:
            if rule(metrics):
                alert = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "severity": "critical",
                    "message": "Alert triggered",
                    "metrics": metrics
                }
                
                self.alert_history.append(alert)
                
                # Send alerts
                for handler in self.alert_handlers:
                    try:
                        handler(alert)
                    except Exception as e:
                        # Log handler error
                        pass

# Example alert rules
def high_error_rate_rule(metrics: Dict) -> bool:
    """Alert if error rate > 5%."""
    total = metrics.get("mcp_requests_total", {}).get("all", 0)
    errors = metrics.get("mcp_requests_total", {}).get("error", 0)
    
    if total > 0:
        error_rate = errors / total
        return error_rate > 0.05
    
    return False

def slow_response_rule(metrics: Dict) -> bool:
    """Alert if p95 latency > 1 second."""
    p95 = metrics.get("mcp_request_duration_ms", {}).get("p95", 0)
    return p95 > 1000

def high_memory_rule(metrics: Dict) -> bool:
    """Alert if memory usage > 80%."""
    memory = metrics.get("memory_usage", {}).get("percent", 0)
    return memory > 80

# Usage
alert_manager = AlertManager()
alert_manager.add_alert_rule(high_error_rate_rule)
alert_manager.add_alert_rule(slow_response_rule)
alert_manager.add_alert_rule(high_memory_rule)

def slack_alert_handler(alert: Dict):
    """Send alert to Slack."""
    # Implementation for Slack notification
    pass

alert_manager.add_alert_handler(slack_alert_handler)