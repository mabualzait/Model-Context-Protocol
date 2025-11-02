# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.8 Protocol Implementation Deep Dive

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