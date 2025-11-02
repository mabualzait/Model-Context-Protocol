# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.8 Protocol Implementation Deep Dive

class JSONRPCNotification:
    """JSON-RPC 2.0 notification structure (no response expected)."""
    
    def __init__(self, method: str, params: Dict = None):
        self.jsonrpc = "2.0"
        self.method = method
        self.params = params or {}
    
    def to_dict(self) -> Dict:
        """Convert to JSON-RPC 2.0 format."""
        result = {
            "jsonrpc": self.jsonrpc,
            "method": self.method
        }
        
        if self.params:
            result["params"] = self.params
        
        return result