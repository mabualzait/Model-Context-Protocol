# 📖 Chapter: Chapter 15: The Future of MCP
# 📖 Section: 15.2 Protocol Evolution and Roadmap

import gzip
import json

class CompressedMCPTransport:
    """MCP transport with compression support."""
    
    def __init__(self):
        self.compression_threshold = 1024  # 1KB
    
    def send_compressed(self, message: Dict) -> bytes:
        """Send message with compression if beneficial."""
        message_json = json.dumps(message).encode()
        
        if len(message_json) > self.compression_threshold:
            compressed = gzip.compress(message_json)
            
            # Only use compression if it reduces size
            if len(compressed) < len(message_json):
                return compressed
        
        return message_json
    
    def receive_compressed(self, data: bytes) -> Dict:
        """Receive and decompress message."""
        try:
            # Try decompression
            decompressed = gzip.decompress(data)
            return json.loads(decompressed)
        except:
            # Fall back to uncompressed
            return json.loads(data)