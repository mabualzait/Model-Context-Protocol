# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.5 Error Handling and Retry Strategies

import signal
from contextlib import contextmanager

@contextmanager
def timeout(seconds):
    """Timeout context manager"""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Operation timed out after {seconds} seconds")
    
    # Set up signal handler
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

class MCPClient:
    def call_tool_with_timeout(self, name, arguments, timeout_seconds=30):
        """Call tool with timeout"""
        try:
            with timeout(timeout_seconds):
                return self.call_tool(name, arguments)
        except TimeoutError:
            raise MCPError(f"Tool call timed out after {timeout_seconds} seconds")