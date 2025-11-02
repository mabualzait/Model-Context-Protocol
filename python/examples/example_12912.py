# 📖 Chapter: Chapter 9: Advanced MCP Patterns
# 📖 Section: 9.2 Async Operations and Streaming

class StreamingMCPClient:
    """MCP client with streaming support."""
    
    def __init__(self, client: MCPClient):
        self.client = client
        self.chunk_size = 8192  # 8KB chunks
    
    def stream_resource(self, uri: str) -> AsyncGenerator[bytes, None]:
        """Stream resource content in chunks."""
        # Subscribe to resource updates
        subscription = self.client.subscribe_resource(uri)
        
        async def stream_generator():
            try:
                while True:
                    chunk = await subscription.get_next()
                    if chunk is None:
                        break
                    yield chunk
            finally:
                subscription.cancel()
        
        return stream_generator()
    
    async def stream_large_file(self, file_uri: str, 
                               output_path: str):
        """Stream large file to disk."""
        async with aiofiles.open(output_path, 'wb') as f:
            async for chunk in self.stream_resource(file_uri):
                await f.write(chunk)