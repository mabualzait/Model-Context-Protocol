# 📖 Chapter: Chapter 11: Monitoring and Observability
# 📖 Section: 11.4 Performance Profiling

import cProfile
import pstats
import io
from functools import wraps

class PerformanceProfiler:
    """Profile MCP request performance."""
    
    def __init__(self):
        self.profiles: Dict[str, cProfile.Profile] = {}
    
    def profile_request(self, request_id: str):
        """Profile decorator for requests."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                profiler = cProfile.Profile()
                profiler.enable()
                
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    profiler.disable()
                    self.profiles[request_id] = profiler
            
            return wrapper
        return decorator
    
    def get_profile_stats(self, request_id: str) -> str:
        """Get profile statistics."""
        if request_id not in self.profiles:
            return None
        
        profiler = self.profiles[request_id]
        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Top 20 functions
        
        return stream.getvalue()
    
    def analyze_slow_requests(self, threshold_ms: float = 1000) -> List[Dict]:
        """Find requests slower than threshold."""
        slow_requests = []
        
        for request_id, profiler in self.profiles.items():
            stats = pstats.Stats(profiler)
            total_time = stats.total_tt
            
            if total_time * 1000 > threshold_ms:  # Convert to ms
                slow_requests.append({
                    "request_id": request_id,
                    "duration_ms": total_time * 1000,
                    "stats": self.get_profile_stats(request_id)
                })
        
        return sorted(slow_requests, key=lambda x: x["duration_ms"], reverse=True)