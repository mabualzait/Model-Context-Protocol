# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.3 Resources: Providing Data Access

import os
from pathlib import Path

class FileSystemResourceServer:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.resources = {}
    
    def list_resources(self):
        """List all files in root path"""
        resources = []
        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                uri = f"file://{file_path}"
                resources.append({
                    "uri": uri,
                    "name": file_path.name,
                    "mimeType": self._get_mime_type(file_path),
                    "description": f"File at {file_path}"
                })
        return {"resources": resources}
    
    def read_resource(self, uri):
        """Read file contents"""
        if not uri.startswith("file://"):
            raise ValueError(f"Invalid URI: {uri}")
        
        path = Path(uri[7:])  # Remove "file://" prefix
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        with open(path, 'r') as f:
            content = f.read()
        
        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": self._get_mime_type(path),
                    "text": content
                }
            ]
        }
    
    def _get_mime_type(self, path):
        """Get MIME type for file"""
        # Simplified implementation
        ext = path.suffix.lower()
        mime_types = {
            ".txt": "text/plain",
            ".py": "text/x-python",
            ".js": "text/javascript",
            ".json": "application/json",
            ".html": "text/html",
            ".css": "text/css"
        }
        return mime_types.get(ext, "text/plain")