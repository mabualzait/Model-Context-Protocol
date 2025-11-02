# 📖 Chapter: Chapter 2: The Architecture of MCP
# 📖 Section: 2.10 Protocol Extension Mechanisms

class ExtendedMCPServer:
    """MCP server with custom protocol extensions."""
    
    def __init__(self):
        self.extensions: Dict[str, Extension] = {}
        self.custom_methods: Dict[str, Callable] = {}
    
    def register_extension(self, extension_name: str, extension: 'Extension'):
        """Register protocol extension."""
        self.extensions[extension_name] = extension
        self.custom_methods.update(extension.get_methods())
    
    def initialize(self, request: Dict) -> Dict:
        """Initialize with extension capabilities."""
        client_capabilities = request.get("capabilities", {})
        
        # Standard capabilities
        server_capabilities = {
            "tools": {},
            "resources": {},
            "prompts": {}
        }
        
        # Add extension capabilities
        for ext_name, ext in self.extensions.items():
            if ext.is_supported_by_client(client_capabilities):
                server_capabilities[ext_name] = ext.get_capabilities()
        
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": server_capabilities,
            "serverInfo": {
                "name": "extended-server",
                "version": "1.0.0"
            }
        }
    
    def handle_custom_method(self, method: str, params: Dict) -> Any:
        """Handle custom extension methods."""
        if method in self.custom_methods:
            handler = self.custom_methods[method]
            return handler(params)
        else:
            raise ValueError(f"Unknown method: {method}")

class Extension:
    """Base class for protocol extensions."""
    
    def get_capabilities(self) -> Dict:
        """Return extension capabilities."""
        raise NotImplementedError
    
    def is_supported_by_client(self, client_capabilities: Dict) -> bool:
        """Check if client supports this extension."""
        raise NotImplementedError
    
    def get_methods(self) -> Dict[str, Callable]:
        """Return extension methods."""
        raise NotImplementedError

# Example: Streaming Extension
class StreamingExtension(Extension):
    """Extension for streaming large data."""
    
    def get_capabilities(self) -> Dict:
        return {
            "streaming": {
                "enabled": True,
                "chunkSize": 1024
            }
        }
    
    def is_supported_by_client(self, client_capabilities: Dict) -> bool:
        return "streaming" in client_capabilities
    
    def get_methods(self) -> Dict[str, Callable]:
        return {
            "resources/stream": self.stream_resource
        }
    
    def stream_resource(self, params: Dict) -> Iterator[Dict]:
        """Stream resource in chunks."""
        uri = params["uri"]
        chunk_size = params.get("chunkSize", 1024)
        
        # Stream resource data
        with open(uri.replace("file://", ""), 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                yield {
                    "chunk": chunk.hex(),  # Or base64, etc.
                    "complete": False
                }
            
            yield {"complete": True}