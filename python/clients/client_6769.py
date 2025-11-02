# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.8 Comprehensive Error Handling

class MCPError(Exception):
    """Base exception for MCP errors."""
    pass

class MCPConnectionError(MCPError):
    """Connection-related errors."""
    pass

class MCPProtocolError(MCPError):
    """Protocol-level errors."""
    pass

class MCPServerError(MCPError):
    """Server-side errors."""
    def __init__(self, message: str, error_code: int, error_data: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.error_data = error_data

class MCPTimeoutError(MCPError):
    """Timeout errors."""
    pass

class MCPAuthenticationError(MCPError):
    """Authentication errors."""
    pass

class ErrorHandler:
    """Centralized error handling."""
    
    @staticmethod
    def handle_error(error: Exception) -> Dict:
        """Handle error and return appropriate response."""
        if isinstance(error, MCPConnectionError):
            return {
                "type": "connection_error",
                "retryable": True,
                "message": str(error),
                "action": "retry_connection"
            }
        
        elif isinstance(error, MCPServerError):
            return {
                "type": "server_error",
                "retryable": error.error_code in [-32603, -32600],  # Internal error, Invalid Request
                "message": str(error),
                "error_code": error.error_code,
                "action": "retry_request" if error.error_code == -32603 else "fix_request"
            }
        
        elif isinstance(error, MCPTimeoutError):
            return {
                "type": "timeout_error",
                "retryable": True,
                "message": str(error),
                "action": "retry_with_backoff"
            }
        
        else:
            return {
                "type": "unknown_error",
                "retryable": False,
                "message": str(error),
                "action": "log_and_notify"
            }