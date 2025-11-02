# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.4 Tool Invocation Patterns

import asyncio
from typing import Callable, Optional

class AsyncMCPClient:
    async def call_tool_async(self, name, arguments, progress_callback: Optional[Callable] = None):
        """Call tool asynchronously with progress support"""
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        
        # Send request
        response = await self._send_request_async(request)
        
        # Handle progress notifications
        if progress_callback:
            await self._handle_progress(progress_callback)
        
        return response["result"]
    
    async def _handle_progress(self, callback):
        """Handle progress notifications"""
        while True:
            notification = await self._receive_notification()
            if notification.get("method") == "notifications/progress":
                callback(notification["params"])
            elif notification.get("method") == "notifications/completion":
                break