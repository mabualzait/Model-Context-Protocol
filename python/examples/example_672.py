# 📖 Chapter: Chapter 1: Introduction to Model Context Protocol
# 📖 Section: 1.8 Technical Deep Dive: How MCP Works

class MCPErrorHandler:
    """Error handling for MCP operations."""
    
    ERROR_CODES = {
        # JSON-RPC 2.0 standard errors
        -32700: "Parse error",
        -32600: "Invalid Request",
        -32601: "Method not found",
        -32602: "Invalid params",
        -32603: "Internal error",
        
        # MCP-specific errors
        -32000: "General MCP error",
        -32001: "Resource not found",
        -32002: "Tool execution failed",
        -32003: "Invalid resource URI",
        -32004: "Permission denied",
        -32005: "Rate limit exceeded"
    }
    
    @classmethod
    def handle_error(cls, error_code: int, error_message: str, error_data: Optional[Dict] = None):
        """Handle MCP error."""
        error_type = cls.ERROR_CODES.get(error_code, "Unknown error")
        
        if error_code == -32004:  # Permission denied
            raise PermissionError(f"{error_type}: {error_message}")
        elif error_code == -32001:  # Resource not found
            raise FileNotFoundError(f"{error_type}: {error_message}")
        elif error_code in [-32603, -32002]:  # Internal/Tool execution error
            raise RuntimeError(f"{error_type}: {error_message}")
        else:
            raise ValueError(f"{error_type}: {error_message}")