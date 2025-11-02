# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.6 Production Deployment Considerations

import signal
import threading

class GracefulShutdownManager:
    """Manage graceful shutdown of MCP server."""
    
    def __init__(self, server: 'MCPServer'):
        self.server = server
        self.shutdown_event = threading.Event()
        self.active_requests = 0
        self.lock = threading.Lock()
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"Received signal {signum}, initiating graceful shutdown...")
        self.shutdown_event.set()
    
    def wait_for_shutdown(self, timeout: int = 30):
        """Wait for graceful shutdown."""
        # Stop accepting new connections
        self.server.stop_accepting_connections()
        
        # Wait for active requests to complete
        start_time = time.time()
        while time.time() - start_time < timeout:
            with self.lock:
                if self.active_requests == 0:
                    break
            
            time.sleep(0.1)
        
        # Force shutdown if timeout
        if time.time() - start_time >= timeout:
            print("Timeout reached, forcing shutdown")
        
        # Cleanup
        self.server.cleanup()
        print("Server shutdown complete")
    
    def track_request(self):
        """Track active request."""
        with self.lock:
            self.active_requests += 1
    
    def untrack_request(self):
        """Untrack completed request."""
        with self.lock:
            self.active_requests -= 1