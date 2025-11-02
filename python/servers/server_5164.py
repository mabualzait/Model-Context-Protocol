# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.7 Advanced Server Patterns

import asyncio
from typing import Dict, Any, List
from mcp import Server, Resource, Tool

class AsyncMCPServer:
    """Async MCP server implementation."""
    
    def __init__(self):
        self.server = Server(name="async-server", version="1.0.0")
        self.resources: Dict[str, str] = {}
        self.tools: Dict[str, callable] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.running = False
    
    async def start(self):
        """Start async server."""
        self.running = True
        
        # Start request handler
        asyncio.create_task(self._handle_requests())
        
        # Start listening for requests (stdio or HTTP)
        await self._listen()
    
    async def _listen(self):
        """Listen for incoming requests."""
        while self.running:
            try:
                # In real implementation, read from stdin or HTTP endpoint
                request = await self._read_request()
                await self.task_queue.put(request)
            except asyncio.CancelledError:
                break
    
    async def _handle_requests(self):
        """Handle requests from queue."""
        while self.running:
            try:
                request = await self.task_queue.get()
                response = await self._process_request(request)
                await self._send_response(response)
                self.task_queue.task_done()
            except asyncio.CancelledError:
                break
    
    async def _process_request(self, request: Dict) -> Dict:
        """Process request asynchronously."""
        method = request.get("method")
        
        if method == "initialize":
            return await self._handle_initialize(request)
        elif method == "resources/list":
            return await self._handle_list_resources(request)
        elif method == "resources/read":
            return await self._handle_read_resource(request)
        elif method == "tools/list":
            return await self._handle_list_tools(request)
        elif method == "tools/call":
            return await self._handle_call_tool(request)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    async def _handle_initialize(self, request: Dict) -> Dict:
        """Handle initialize request."""
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "serverInfo": {
                    "name": "async-server",
                    "version": "1.0.0"
                }
            }
        }
    
    async def _handle_list_resources(self, request: Dict) -> Dict:
        """Handle list resources request."""
        resources = list(self.resources.keys())
        
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "resources": resources
            }
        }
    
    async def _handle_read_resource(self, request: Dict) -> Dict:
        """Handle read resource request."""
        uri = request.get("params", {}).get("uri")
        
        if uri not in self.resources:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32001,
                    "message": f"Resource not found: {uri}"
                }
            }
        
        content = self.resources[uri]
        
        # Simulate async operation (e.g., reading from database)
        await asyncio.sleep(0.01)  # Simulate I/O
        
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "contents": [{
                    "uri": uri,
                    "mimeType": "text/plain",
                    "text": content
                }]
            }
        }
    
    async def _handle_list_tools(self, request: Dict) -> Dict:
        """Handle list tools request."""
        tools = [
            {
                "name": name,
                "description": func.__doc__ or "",
                "inputSchema": {}
            }
            for name, func in self.tools.items()
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "tools": tools
            }
        }
    
    async def _handle_call_tool(self, request: Dict) -> Dict:
        """Handle tool call request."""
        params = request.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in self.tools:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32002,
                    "message": f"Tool not found: {tool_name}"
                }
            }
        
        tool_func = self.tools[tool_name]
        
        try:
            # Call tool (supports both sync and async tools)
            if asyncio.iscoroutinefunction(tool_func):
                result = await tool_func(**arguments)
            else:
                # Run sync tool in executor
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,
                    lambda: tool_func(**arguments)
                )
            
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(result)
                    }]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "content": [{
                        "type": "text",
                        "text": f"Error: {str(e)}"
                    }],
                    "isError": True
                }
            }
    
    async def _read_request(self) -> Dict:
        """Read request from transport."""
        # In real implementation, read from stdin or HTTP
        # This is a placeholder
        await asyncio.sleep(0.1)
        return {}
    
    async def _send_response(self, response: Dict):
        """Send response via transport."""
        # In real implementation, write to stdout or HTTP
        pass