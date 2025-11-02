# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.8 Protocol Implementation Deep Dive

class JSONRPCResponse:
    """JSON-RPC 2.0 response structure."""
    
    def __init__(self, request_id: int, result: Any = None, error: Dict = None):
        self.jsonrpc = "2.0"
        self.id = request_id
        self.result = result
        self.error = error
    
    @classmethod
    def success(cls, request_id: int, result: Any):
        """Create success response."""
        return cls(request_id=request_id, result=result)
    
    @classmethod
    def error_response(cls, request_id: int, code: int, message: str, data: Any = None):
        """Create error response."""
        error = {
            "code": code,
            "message": message
        }
        if data is not None:
            error["data"] = data
        
        return cls(request_id=request_id, error=error)
    
    def to_dict(self) -> Dict:
        """Convert to JSON-RPC 2.0 format."""
        result = {
            "jsonrpc": self.jsonrpc,
            "id": self.id
        }
        
        if self.error:
            result["error"] = self.error
        else:
            result["result"] = self.result
        
        return result