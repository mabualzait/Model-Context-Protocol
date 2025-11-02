# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.4 Advanced Testing Strategies

import time
import statistics
from concurrent.futures import ThreadPoolExecutor

class PerformanceTestSuite:
    """Performance testing for MCP server."""
    
    def __init__(self, client: 'MCPClient'):
        self.client = client
    
    def test_concurrent_requests(self, num_requests: int = 100) -> Dict:
        """Test concurrent request handling."""
        latencies = []
        
        def make_request():
            start = time.time()
            self.client.call_tool("read_file", {"path": "test.txt"})
            latencies.append(time.time() - start)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(make_request)
                for _ in range(num_requests)
            ]
            
            for future in futures:
                future.result()
        
        return {
            "total_requests": num_requests,
            "mean_latency": statistics.mean(latencies),
            "median_latency": statistics.median(latencies),
            "p95_latency": statistics.quantiles(latencies, n=20)[18],
            "p99_latency": statistics.quantiles(latencies, n=100)[98],
            "min_latency": min(latencies),
            "max_latency": max(latencies)
        }
    
    def test_throughput(self, duration_seconds: int = 10) -> Dict:
        """Test request throughput."""
        requests_completed = 0
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        while time.time() < end_time:
            self.client.call_tool("read_file", {"path": "test.txt"})
            requests_completed += 1
        
        actual_duration = time.time() - start_time
        
        return {
            "requests_completed": requests_completed,
            "duration_seconds": actual_duration,
            "requests_per_second": requests_completed / actual_duration
        }