# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.5 Troubleshooting Common Issues

import cProfile
import pstats
import io

class PerformanceProfiler:
    """Profile MCP server performance."""
    
    def profile_server_operation(self, operation: callable, *args, **kwargs):
        """Profile a server operation."""
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = operation(*args, **kwargs)
        
        profiler.disable()
        
        # Generate profiling report
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s)
        ps.sort_stats('cumulative')
        ps.print_stats(20)  # Top 20 functions
        
        print(s.getvalue())
        
        return result