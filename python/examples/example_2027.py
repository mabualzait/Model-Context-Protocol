# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.8 Performance and Scalability Considerations

class BatchedMCPClient:
    """MCP client with request batching."""
    
    def __init__(self, client: 'MCPClient'):
        self.client = client
        self.batch_window = 0.1  # 100ms batching window
        self.pending_requests: List[Dict] = []
        self.batch_timer = None
    
    def call_tool_batched(self, name: str, arguments: Dict) -> 'Future':
        """Add tool call to batch."""
        future = Future()
        
        request = {
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
            "future": future
        }
        
        self.pending_requests.append(request)
        
        # Trigger batch if window expired
        if not self.batch_timer:
            self.batch_timer = Timer(self.batch_window, self._flush_batch)
            self.batch_timer.start()
        
        return future
    
    def _flush_batch(self):
        """Flush pending batch of requests."""
        if not self.pending_requests:
            return
        
        # Execute batch
        results = self.client.batch_call(self.pending_requests)
        
        # Resolve futures
        for request, result in zip(self.pending_requests, results):
            request["future"].set_result(result)
        
        self.pending_requests.clear()
        self.batch_timer = None