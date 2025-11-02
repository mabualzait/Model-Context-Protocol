# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.2 Implementing Resources

from pathlib import Path
from typing import List, Optional
from mcp import Resource

class FileSystemResources:
    """File system resource implementation."""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        if not self.root_path.exists():
            raise ValueError(f"Root path does not exist: {root_path}")
    
    def list_resources(self) -> List[Resource]:
        """List all files in root path as resources."""
        resources = []
        
        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                uri = f"file://{file_path}"
                resources.append(Resource(
                    uri=uri,
                    name=file_path.name,
                    mimeType=self._get_mime_type(file_path),
                    description=f"File at {file_path}"
                ))
        
        return resources
    
    def read_resource(self, uri: str) -> str:
        """Read file content."""
        if not uri.startswith("file://"):
            raise ValueError(f"Invalid URI: {uri}")
        
        path = Path(uri[7:])  # Remove "file://" prefix
        
        # Security check: ensure path is within root
        try:
            path = path.resolve()
            if not path.is_relative_to(self.root_path):
                raise PermissionError(f"Access denied: path outside root")
        except ValueError:
            raise PermissionError(f"Access denied: invalid path")
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            raise ValueError(f"Cannot read binary file as text: {path}")
    
    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file."""
        ext = path.suffix.lower()
        mime_types = {
            ".txt": "text/plain",
            ".py": "text/x-python",
            ".js": "text/javascript",
            ".ts": "text/typescript",
            ".json": "application/json",
            ".html": "text/html",
            ".css": "text/css",
            ".md": "text/markdown",
            ".yaml": "text/yaml",
            ".yml": "text/yaml",
            ".xml": "application/xml",
        }
        return mime_types.get(ext, "application/octet-stream")