# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.4 Advanced Testing Strategies

class LoadTestRunner:
    """Load testing for MCP server."""
    
    def __init__(self, client: 'MCPClient'):
        self.client = client
    
    def run_load_test(self, 
                     concurrent_users: int = 50,
                     requests_per_user: int = 100,
                     ramp_up_seconds: int = 10) -> Dict:
        """Run load test simulation."""
        results = {
            "successful_requests": 0,
            "failed_requests": 0,
            "total_latency": 0,
            "errors": []
        }
        
        def user_simulation(user_id: int):
            """Simulate user behavior."""
            user_results = {
                "successful": 0,
                "failed": 0,
                "errors": []
            }
            
            for i in range(requests_per_user):
                try:
                    start = time.time()
                    result = self.client.call_tool("read_file", {"path": f"user_{user_id}_file_{i}.txt"})
                    latency = time.time() - start
                    
                    user_results["successful"] += 1
                    results["successful_requests"] += 1
                    results["total_latency"] += latency
                except Exception as e:
                    user_results["failed"] += 1
                    results["failed_requests"] += 1
                    results["errors"].append(str(e))
                
                # Small delay between requests
                time.sleep(0.01)
            
            return user_results
        
        # Ramp up users gradually
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = []
            
            for user_id in range(concurrent_users):
                # Stagger user start times
                delay = (user_id / concurrent_users) * ramp_up_seconds
                time.sleep(delay / concurrent_users)
                
                future = executor.submit(user_simulation, user_id)
                futures.append(future)
            
            # Wait for all users to complete
            for future in futures:
                future.result()
        
        results["average_latency"] = (
            results["total_latency"] / results["successful_requests"]
            if results["successful_requests"] > 0 else 0
        )
        results["error_rate"] = (
            results["failed_requests"] / 
            (results["successful_requests"] + results["failed_requests"])
            if (results["successful_requests"] + results["failed_requests"]) > 0 else 0
        )
        
        return results