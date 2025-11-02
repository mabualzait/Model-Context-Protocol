# 📖 Chapter: Chapter 11: Monitoring and Observability
# 📖 Section: 11.1 Logging Strategies

from typing import List
import requests

class LogAggregator:
    """Aggregate logs from multiple MCP services."""
    
    def __init__(self, aggregation_endpoint: str):
        self.endpoint = aggregation_endpoint
        self.log_buffer: List[Dict] = []
        self.buffer_size = 100
    
    def send_log(self, log_entry: Dict):
        """Send log entry to aggregation service."""
        self.log_buffer.append(log_entry)
        
        if len(self.log_buffer) >= self.buffer_size:
            self.flush_logs()
    
    def flush_logs(self):
        """Flush buffered logs."""
        if not self.log_buffer:
            return
        
        try:
            response = requests.post(
                self.endpoint,
                json={"logs": self.log_buffer},
                timeout=5
            )
            response.raise_for_status()
            self.log_buffer.clear()
        except Exception as e:
            # Retry logic or local storage
            pass