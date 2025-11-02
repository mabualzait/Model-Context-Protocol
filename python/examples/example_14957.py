# 📖 Chapter: Chapter 11: Monitoring and Observability
# 📖 Section: 11.3 Debugging Distributed MCP Systems

class RequestCorrelator:
    """Correlate requests across services."""
    
    def __init__(self):
        self.correlations: Dict[str, List[str]] = {}  # trace_id -> [request_ids]
    
    def correlate_request(self, trace_id: str, request_id: str):
        """Correlate request to trace."""
        if trace_id not in self.correlations:
            self.correlations[trace_id] = []
        
        self.correlations[trace_id].append(request_id)
    
    def get_trace_requests(self, trace_id: str) -> List[str]:
        """Get all requests for trace."""
        return self.correlations.get(trace_id, [])
    
    def search_by_request_id(self, request_id: str) -> Optional[str]:
        """Find trace ID for request."""
        for trace_id, request_ids in self.correlations.items():
            if request_id in request_ids:
                return trace_id
        return None