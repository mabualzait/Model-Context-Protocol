# 📖 Chapter: Chapter 9: Advanced MCP Patterns
# 📖 Section: 9.2 Async Operations and Streaming

import asyncio
from typing import AsyncGenerator, Dict, List
from queue import Queue

class AsyncMCPClient:
    """Async MCP client for concurrent operations."""
    
    def __init__(self, endpoint: str, transport: str = 'stdio'):
        self.endpoint = endpoint
        self.transport = transport
        self.client: Optional[MCPClient] = None
        self.request_queue: asyncio.Queue = asyncio.Queue()
        self.response_map: Dict[str, asyncio.Future] = {}
        self.message_id = 0
    
    async def connect(self):
        """Connect to MCP server asynchronously."""
        loop = asyncio.get_event_loop()
        self.client = await loop.run_in_executor(
            None,
            lambda: MCPClient(self.endpoint, self.transport)
        )
        await loop.run_in_executor(None, self.client.connect)
        
        # Start response handler
        asyncio.create_task(self._handle_responses())
    
    async def _handle_responses(self):
        """Handle responses from MCP server."""
        while True:
            try:
                # In real implementation, read from connection
                # For now, this is a placeholder
                await asyncio.sleep(0.1)
                # Process responses from queue
            except asyncio.CancelledError:
                break
    
    async def list_resources_async(self) -> List[Dict]:
        """List resources asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.list_resources
        )
    
    async def read_resource_async(self, uri: str) -> str:
        """Read resource asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.read_resource,
            uri
        )
    
    async def call_tool_async(self, tool_name: str, arguments: Dict) -> Dict:
        """Call tool asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.client.call_tool,
            tool_name,
            arguments
        )
    
    async def batch_operations(self, operations: List[Dict]) -> List[Dict]:
        """Execute multiple operations concurrently."""
        tasks = []
        
        for op in operations:
            if op['type'] == 'read_resource':
                task = self.read_resource_async(op['uri'])
            elif op['type'] == 'call_tool':
                task = self.call_tool_async(op['tool_name'], op['arguments'])
            else:
                task = asyncio.create_task(
                    asyncio.sleep(0)  # Placeholder
                )
            
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [
            {
                'operation': op,
                'result': result if not isinstance(result, Exception) else {'error': str(result)},
                'status': 'success' if not isinstance(result, Exception) else 'error'
            }
            for op, result in zip(operations, results)
        ]