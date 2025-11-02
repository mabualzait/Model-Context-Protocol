# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.7 Advanced Server Patterns

class MiddlewareMCPServer:
    """MCP server with middleware support."""
    
    def __init__(self):
        self.middleware_stack: List[callable] = []
        self.handlers: Dict[str, callable] = {}
    
    def use(self, middleware: callable):
        """Add middleware to stack."""
        self.middleware_stack.append(middleware)
    
    def register_handler(self, method: str, handler: callable):
        """Register handler for method."""
        self.handlers[method] = handler
    
    def handle_request(self, request: Dict) -> Dict:
        """Handle request through middleware stack."""
        # Build handler chain
        handler = self.handlers.get(request.get("method"))
        if not handler:
            return self._error_response(
                request.get("id"),
                -32601,
                "Method not found"
            )
        
        # Wrap handler with middleware
        chain = handler
        for middleware in reversed(self.middleware_stack):
            chain = lambda h=chain, m=middleware: m(h)
        
        try:
            result = chain(request.get("params", {}))
            return self._success_response(request.get("id"), result)
        except Exception as e:
            return self._error_response(request.get("id"), -32603, str(e))
    
    def _success_response(self, request_id: int, result: Any) -> Dict:
        """Create success response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
    
    def _error_response(self, request_id: int, code: int, message: str) -> Dict:
        """Create error response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }

# Example middleware
def logging_middleware(handler: callable) -> callable:
    """Middleware for request logging."""
    def wrapper(params: Dict) -> Any:
        logger.info(f"Request: {params}")
        start_time = time.time()
        
        try:
            result = handler(params)
            duration = time.time() - start_time
            logger.info(f"Request completed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Request failed after {duration:.3f}s: {e}")
            raise
    
    return wrapper

def authentication_middleware(handler: callable) -> callable:
    """Middleware for authentication."""
    def wrapper(params: Dict) -> Any:
        token = params.get("token")
        
        if not self.validate_token(token):
            raise PermissionError("Invalid authentication token")
        
        # Remove token from params before passing to handler
        params_without_token = {k: v for k, v in params.items() if k != "token"}
        return handler(params_without_token)
    
    return wrapper