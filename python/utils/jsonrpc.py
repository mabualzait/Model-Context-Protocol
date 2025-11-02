# 📁 File: python/utils/jsonrpc.py
# 📖 Chapter 2, Section 2.8: Protocol Implementation Deep Dive
# 🔗 GitHub: https://github.com/mabualzait/Model-Context-Protocol/blob/main/python/utils/jsonrpc.py

# JSON-RPC 2.0 Implementation
import json
from typing import Dict, Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)

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


class MCPMessageHandler:
    """Handler for MCP protocol messages."""
    
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self.request_id_counter = 0
        self.pending_requests: Dict[int, Dict] = {}
    
    def register_handler(self, method: str, handler: Callable):
        """Register handler for MCP method."""
        self.handlers[method] = handler
    
    def handle_message(self, message: Dict) -> Optional[Dict]:
        """Handle incoming JSON-RPC message."""
        if not message.get("jsonrpc") == "2.0":
            return self._error_response(
                message.get("id"),
                -32700,
                "Parse error: Invalid JSON-RPC version"
            )
        
        # Check if it's a request or notification
        if "id" in message and "method" in message:
            # It's a request (expects response)
            return self._handle_request(message)
        elif "method" in message:
            # It's a notification (no response)
            self._handle_notification(message)
            return None
        elif "id" in message and ("result" in message or "error" in message):
            # It's a response
            return self._handle_response(message)
        else:
            return self._error_response(
                message.get("id"),
                -32600,
                "Invalid Request: Malformed message"
            )
    
    def _handle_request(self, message: Dict) -> Dict:
        """Handle request message."""
        method = message.get("method")
        params = message.get("params", {})
        request_id = message.get("id")
        
        # Check if method is registered
        if method not in self.handlers:
            return self._error_response(
                request_id,
                -32601,
                "Method not found",
                {"method": method}
            )
        
        # Execute handler
        try:
            handler = self.handlers[method]
            result = handler(params)
            return self._success_response(request_id, result)
        except Exception as e:
            logger.error(f"Error handling request {method}: {e}")
            return self._error_response(
                request_id,
                -32603,
                "Internal error",
                {"message": str(e)}
            )
    
    def _handle_notification(self, message: Dict):
        """Handle notification message."""
        method = message.get("method")
        params = message.get("params", {})
        
        if method in self.handlers:
            try:
                handler = self.handlers[method]
                handler(params)
            except Exception as e:
                logger.error(f"Error handling notification {method}: {e}")
    
    def _handle_response(self, message: Dict):
        """Handle response message."""
        request_id = message.get("id")
        
        if request_id in self.pending_requests:
            request_info = self.pending_requests.pop(request_id)
            if "error" in message:
                request_info["error_callback"](message["error"])
            else:
                request_info["success_callback"](message.get("result"))
    
    def send_request(self, method: str, params: Dict = None, 
                    success_callback: Callable = None,
                    error_callback: Callable = None) -> int:
        """Send request and register callbacks."""
        request_id = self._get_next_request_id()
        
        request = JSONRPCRequest(method, params, request_id)
        
        if success_callback or error_callback:
            self.pending_requests[request_id] = {
                "success_callback": success_callback or (lambda x: None),
                "error_callback": error_callback or (lambda x: None)
            }
        
        return request_id
    
    def _success_response(self, request_id: int, result: Any) -> Dict:
        """Create success response."""
        return JSONRPCResponse.success(request_id, result).to_dict()
    
    def _error_response(self, request_id: Optional[int], code: int, message: str, data: Any = None) -> Dict:
        """Create error response."""
        return JSONRPCResponse.error_response(request_id, code, message, data).to_dict()
    
    def _get_next_request_id(self) -> int:
        """Get next request ID."""
        self.request_id_counter += 1
        return self.request_id_counter

