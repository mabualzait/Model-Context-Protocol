# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.8 Protocol Implementation Deep Dive

class JSONRPCRequest:
    """JSON-RPC 2.0 request structure."""
    
    def __init__(self, method: str, params: Dict = None, request_id: int = None):
        self.jsonrpc = "2.0"
        self.method = method
        self.params = params or {}
        self.id = request_id
    
    def to_dict(self) -> Dict:
        """Convert to JSON-RPC 2.0 format."""
        result = {
            "jsonrpc": self.jsonrpc,
            "method": self.method
        }
        
        if self.params:
            result["params"] = self.params
        
        if self.id is not None:
            result["id"] = self.id
        
        return result
    
    def to_json(self) -> str:
        """Serialize to JSON."""
        return json.dumps(self.to_dict())