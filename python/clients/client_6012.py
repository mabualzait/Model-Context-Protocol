# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.5 Error Handling and Retry Strategies

class MCPError(Exception):
    """Base MCP error"""
    pass

class MCPConnectionError(MCPError):
    """Connection-related errors"""
    pass

class MCPProtocolError(MCPError):
    """Protocol-related errors"""
    pass

class MCPToolError(MCPError):
    """Tool execution errors"""
    pass

class MCPClient:
    def _handle_error(self, response):
        """Handle error response"""
        error = response.get("error")
        if not error:
            return None
        
        code = error.get("code")
        message = error.get("message")
        data = error.get("data")
        
        # Standard JSON-RPC error codes
        if code == -32700:
            raise MCPProtocolError("Parse error")
        elif code == -32600:
            raise MCPProtocolError("Invalid request")
        elif code == -32601:
            raise MCPProtocolError(f"Method not found: {data}")
        elif code == -32602:
            raise MCPProtocolError(f"Invalid params: {data}")
        elif code == -32603:
            raise MCPToolError(f"Internal error: {data}")
        else:
            raise MCPError(f"Error {code}: {message} - {data}")