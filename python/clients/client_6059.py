# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.5 Error Handling and Retry Strategies

import time
from functools import wraps

def retry_with_backoff(max_retries=3, initial_delay=1.0, backoff_factor=2.0):
    """Retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (MCPConnectionError, ConnectionError) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        raise
            
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator

class MCPClient:
    @retry_with_backoff(max_retries=3)
    def call_tool(self, name, arguments):
        """Call tool with retry logic"""
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        
        response = self._send_request(request)
        
        if response.get("error"):
            error = response["error"]
            code = error.get("code")
            
            # Retry on connection errors
            if code in [-32000, -32001]:  # Connection errors
                raise MCPConnectionError(error.get("message"))
            
            raise MCPToolError(error.get("message"))
        
        return response["result"]