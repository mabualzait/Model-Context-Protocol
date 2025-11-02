# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.9 Advanced Transport Mechanisms

class WebSocketMCPTransport:
    """WebSocket-based MCP transport."""
    
    def __init__(self, url: str):
        self.url = url
        self.ws = None
        self.connected = False
        self.message_queue: List[Dict] = []
        self.received_messages: Dict[int, Dict] = {}
        self.message_handlers: Dict[str, Callable] = {}
    
    async def connect(self):
        """Connect to WebSocket server."""
        import websockets
        
        self.ws = await websockets.connect(self.url)
        self.connected = True
        
        # Start message receiver
        asyncio.create_task(self._receive_messages())
    
    async def send_request(self, method: str, params: Dict = None) -> Dict:
        """Send request and wait for response."""
        request_id = self._get_next_request_id()
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params or {}
        }
        
        await self.ws.send(json.dumps(request))
        
        # Wait for response
        while request_id not in self.received_messages:
            await asyncio.sleep(0.01)
        
        response = self.received_messages.pop(request_id)
        
        if "error" in response:
            raise MCPError(response["error"])
        
        return response.get("result")
    
    async def send_notification(self, method: str, params: Dict = None):
        """Send notification (no response expected)."""
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {}
        }
        
        await self.ws.send(json.dumps(notification))
    
    async def _receive_messages(self):
        """Receive and handle messages."""
        while self.connected:
            try:
                message_text = await self.ws.recv()
                message = json.loads(message_text)
                
                if "id" in message:
                    # Response to request
                    self.received_messages[message["id"]] = message
                elif "method" in message:
                    # Notification
                    await self._handle_notification(message)
            except websockets.exceptions.ConnectionClosed:
                self.connected = False
                break
            except Exception as e:
                logger.error(f"Error receiving message: {e}")