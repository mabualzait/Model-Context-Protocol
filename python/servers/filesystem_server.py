# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.7 Real-World Case Study: File Management Server

"""
Production-Ready File Management MCP Server
Example of a complete, real-world MCP server implementation.
"""

from pathlib import Path
import json
import hashlib
import mimetypes
from typing import Dict, List, Optional
from datetime import datetime
import logging
from mcp import Server, Resource, Tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileManagementMCPServer:
    """Production-ready file management MCP server."""
    
    def __init__(self, root_path: str, config: Dict):
        self.root_path = Path(root_path).resolve()
        self.config = config
        self.server = Server(
            name="file-management-server",
            version="1.0.0",
            protocol_version="2024-11-05"
        )
        
        # Metrics
        self.metrics = {
            "requests_total": 0,
            "requests_by_method": {},
            "errors_total": 0,
            "start_time": datetime.now()
        }
        
        # Security
        self.allowed_paths = set(self.config.get("allowed_paths", []))
        self.max_file_size = self.config.get("max_file_size", 10 * 1024 * 1024)  # 10MB
        
        # Initialize handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register MCP handlers."""
        self.server.on_list_resources = self._list_resources
        self.server.on_read_resource = self._read_resource
        self.server.on_list_tools = self._list_tools
        self.server.on_call_tool = self._call_tool
    
    def _list_resources(self) -> List[Resource]:
        """List file system resources."""
        resources = []
        max_resources = self.config.get("max_resources", 1000)
        
        try:
            count = 0
            for file_path in self.root_path.rglob("*"):
                if count >= max_resources:
                    break
                
                if file_path.is_file():
                    uri = f"file://{file_path.relative_to(self.root_path)}"
                    
                    # Security check
                    if not self._is_path_allowed(file_path):
                        continue
                    
                    resources.append(Resource(
                        uri=uri,
                        name=file_path.name,
                        mimeType=self._get_mime_type(file_path),
                        description=f"File: {file_path}"
                    ))
                    count += 1
        
        except Exception as e:
            logger.error(f"Error listing resources: {e}")
        
        return resources
    
    def _read_resource(self, uri: str) -> str:
        """Read file resource."""
        try:
            file_path = self._uri_to_path(uri)
            
            # Security checks
            if not self._is_path_allowed(file_path):
                raise PermissionError(f"Access denied: {uri}")
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {uri}")
            
            # Size check
            size = file_path.stat().st_size
            if size > self.max_file_size:
                raise ValueError(f"File too large: {size} bytes (max: {self.max_file_size})")
            
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"Read resource: {uri} ({len(content)} bytes)")
            return content
        
        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            raise
    
    def _list_tools(self) -> List[Tool]:
        """List available tools."""
        return [
            Tool(
                name="read_file",
                description="Read file contents",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"}
                    },
                    "required": ["path"]
                }
            ),
            Tool(
                name="write_file",
                description="Write file contents",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["path", "content"]
                }
            ),
            Tool(
                name="list_files",
                description="List files in directory",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Directory path"},
                        "recursive": {"type": "boolean", "default": False}
                    },
                    "required": ["path"]
                }
            ),
            Tool(
                name="get_file_info",
                description="Get file metadata",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"}
                    },
                    "required": ["path"]
                }
            )
        ]
    
    def _call_tool(self, name: str, arguments: Dict) -> Dict:
        """Execute tool."""
        self.metrics["requests_total"] += 1
        self.metrics["requests_by_method"][name] = (
            self.metrics["requests_by_method"].get(name, 0) + 1
        )
        
        try:
            if name == "read_file":
                return self._tool_read_file(arguments)
            elif name == "write_file":
                return self._tool_write_file(arguments)
            elif name == "list_files":
                return self._tool_list_files(arguments)
            elif name == "get_file_info":
                return self._tool_get_file_info(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        except Exception as e:
            self.metrics["errors_total"] += 1
            logger.error(f"Tool execution error: {e}")
            return {
                "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                "isError": True
            }
    
    def _tool_read_file(self, args: Dict) -> Dict:
        """Read file tool."""
        path = self._validate_path(args["path"])
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "content": [{"type": "text", "text": content}]
        }
    
    def _tool_write_file(self, args: Dict) -> Dict:
        """Write file tool."""
        path = self._validate_path(args["path"])
        content = args["content"]
        
        # Create directory if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "content": [{"type": "text", "text": f"File written: {path}"}]
        }
    
    def _tool_list_files(self, args: Dict) -> Dict:
        """List files tool."""
        path = self._validate_path(args["path"])
        recursive = args.get("recursive", False)
        
        if not path.is_dir():
            return {
                "content": [{"type": "text", "text": f"Error: {path} is not a directory"}],
                "isError": True
            }
        
        files = []
        if recursive:
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    files.append({
                        "path": str(file_path.relative_to(self.root_path)),
                        "size": file_path.stat().st_size
                    })
        else:
            for file_path in path.iterdir():
                if file_path.is_file():
                    files.append({
                        "path": str(file_path.relative_to(self.root_path)),
                        "size": file_path.stat().st_size
                    })
        
        return {
            "content": [{"type": "text", "text": json.dumps(files, indent=2)}]
        }
    
    def _tool_get_file_info(self, args: Dict) -> Dict:
        """Get file info tool."""
        path = self._validate_path(args["path"])
        
        if not path.exists():
            return {
                "content": [{"type": "text", "text": f"Error: File not found: {path}"}],
                "isError": True
            }
        
        stat = path.stat()
        info = {
            "path": str(path.relative_to(self.root_path)),
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "mime_type": self._get_mime_type(path)
        }
        
        return {
            "content": [{"type": "text", "text": json.dumps(info, indent=2)}]
        }
    
    def _validate_path(self, path_str: str) -> Path:
        """Validate and resolve path."""
        path = (self.root_path / path_str).resolve()
        
        # Security check
        if not path.is_relative_to(self.root_path):
            raise PermissionError(f"Path outside root: {path_str}")
        
        if self.allowed_paths and not any(path.is_relative_to(Path(p)) for p in self.allowed_paths):
            raise PermissionError(f"Path not allowed: {path_str}")
        
        return path
    
    def _uri_to_path(self, uri: str) -> Path:
        """Convert URI to path."""
        if not uri.startswith("file://"):
            raise ValueError(f"Invalid URI: {uri}")
        
        path_str = uri.replace("file://", "")
        return self._validate_path(path_str)
    
    def _is_path_allowed(self, path: Path) -> bool:
        """Check if path is allowed."""
        if not self.allowed_paths:
            return True
        
        return any(path.is_relative_to(Path(p)) for p in self.allowed_paths)
    
    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file."""
        mime_type, _ = mimetypes.guess_type(str(path))
        return mime_type or "application/octet-stream"
    
    def run(self):
        """Run the server."""
        logger.info(f"Starting file management server (root: {self.root_path})")
        self.server.run()

if __name__ == "__main__":
    config = {
        "allowed_paths": ["/tmp/mcp-files"],
        "max_file_size": 10 * 1024 * 1024,
        "max_resources": 1000
    }
    
    server = FileManagementMCPServer("/tmp/mcp-files", config)
    server.run()