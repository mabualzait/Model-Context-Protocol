# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.4 Resource Pooling and Optimization

class BatchableMCPHost(MCPHost):
    def batch_requests(self, session_id: str, requests: List[Dict]) -> List[Dict]:
        """Batch multiple requests"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        responses = []
        
        # Send requests in parallel (if supported)
        if session.supports_batching():
            batch_request = {
                "jsonrpc": "2.0",
                "method": "batch",
                "params": {"requests": requests}
            }
            batch_response = session.route_request(batch_request)
            responses = batch_response.get("result", {}).get("responses", [])
        else:
            # Send sequentially
            for request in requests:
                response = session.route_request(request)
                responses.append(response)
        
        return responses