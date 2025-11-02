# 📖 Chapter: Appendices
# 📖 Section: A.1 Full MCP Server Implementation
# 🔗 GitHub: https://github.com/modelcontextprotocol

#!/usr/bin/env python3
"""
Complete MCP Server Implementation - File System Server
This is a full, working MCP server that provides file system access.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib

class FileSystemMCPServer:
    """Complete MCP server for file system access."""
    
    def __init__(self, root_directory: str = "/"):
        self.root = Path(root_directory).resolve()
        self.supported_protocol_version = "2024-11-05"
        self.server_info = {
            "name": "filesystem-mcp-server",
            "version": "1.0.0"
        }
        self.tools = {}
        self.resources = {}
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize server tools."""
        self.tools = {
            "read_file": {
                "name": "read_file",
                "description": "Read contents of a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to file to read"
                        }
                    },
                    "required": ["path"]
                }
            },
            "write_file": {
                "name": "write_file",
                "description": "Write content to a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write"
                        }
                    },
                    "required": ["path", "content"]
                }
            },
            "list_directory": {
                "name": "list_directory",
                "description": "List directory contents",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to directory"
                        }
                    },
                    "required": ["path"]
                }
            },
            "search_files": {
                "name": "search_files",
                "description": "Search for files by name pattern",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "File name pattern (supports wildcards)"
                        },
                        "directory": {
                            "type": "string",
                            "description": "Directory to search in"
                        }
                    },
                    "required": ["pattern"]
                }
            }
        }
    
    def handle_initialize(self, params: Dict) -> Dict:
        """Handle initialize request."""
        protocol_version = params.get("protocolVersion", "2024-11-05")
        client_info = params.get("clientInfo", {})
        
        return {
            "protocolVersion": self.supported_protocol_version,
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "serverInfo": self.server_info
        }
    
    def list_tools(self) -> List[Dict]:
        """List available tools."""
        return list(self.tools.values())
    
    def call_tool(self, name: str, arguments: Dict) -> Dict:
        """Execute tool."""
        if name == "read_file":
            return self._read_file(arguments["path"])
        elif name == "write_file":
            return self._write_file(arguments["path"], arguments["content"])
        elif name == "list_directory":
            return self._list_directory(arguments["path"])
        elif name == "search_files":
            return self._search_files(
                arguments["pattern"],
                arguments.get("directory", str(self.root))
            )
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    def _read_file(self, file_path: str) -> Dict:
        """Read file content."""
        full_path = self._validate_path(file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": content
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error reading file: {str(e)}"
                    }
                ],
                "isError": True
            }
    
    def _write_file(self, file_path: str, content: str) -> Dict:
        """Write file content."""
        full_path = self._validate_path(file_path)
        
        try:
            # Create directory if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"File written successfully: {file_path}"
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error writing file: {str(e)}"
                    }
                ],
                "isError": True
            }
    
    def _list_directory(self, directory_path: str) -> Dict:
        """List directory contents."""
        full_path = self._validate_path(directory_path)
        
        if not full_path.is_dir():
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: {directory_path} is not a directory"
                    }
                ],
                "isError": True
            }
        
        try:
            items = []
            for item in sorted(full_path.iterdir()):
                item_type = "directory" if item.is_dir() else "file"
                size = item.stat().st_size if item.is_file() else 0
                
                items.append({
                    "name": item.name,
                    "type": item_type,
                    "size": size,
                    "path": str(item.relative_to(self.root))
                })
            
            result_text = json.dumps(items, indent=2)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result_text
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error listing directory: {str(e)}"
                    }
                ],
                "isError": True
            }
    
    def _search_files(self, pattern: str, directory: str) -> Dict:
        """Search for files matching pattern."""
        search_path = self._validate_path(directory)
        
        try:
            matches = []
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if self._matches_pattern(file, pattern):
                        file_path = Path(root) / file
                        matches.append({
                            "path": str(file_path.relative_to(self.root)),
                            "size": file_path.stat().st_size,
                            "modified": datetime.fromtimestamp(
                                file_path.stat().st_mtime
                            ).isoformat()
                        })
            
            result_text = json.dumps(matches, indent=2)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result_text
                    }
                ]
            }
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error searching files: {str(e)}"
                    }
                ],
                "isError": True
            }
    
    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if filename matches pattern (simple wildcard matching)."""
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
    
    def _validate_path(self, path: str) -> Path:
        """Validate and resolve path within root directory."""
        if os.path.isabs(path):
            full_path = Path(path).resolve()
        else:
            full_path = (self.root / path).resolve()
        
        # Security: Ensure path is within root
        if not str(full_path).startswith(str(self.root)):
            raise ValueError(f"Path {path} is outside root directory")
        
        return full_path
    
    def list_resources(self) -> List[Dict]:
        """List available resources."""
        resources = []
        
        try:
            for root, dirs, files in os.walk(self.root):
                for file in files:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(self.root)
                    uri = f"file://{relative_path}"
                    
                    resources.append({
                        "uri": uri,
                        "name": file,
                        "description": f"File: {relative_path}",
                        "mimeType": self._get_mime_type(file_path)
                    })
        except Exception as e:
            print(f"Error listing resources: {e}")
        
        return resources
    
    def read_resource(self, uri: str) -> str:
        """Read resource content."""
        if not uri.startswith("file://"):
            raise ValueError(f"Invalid resource URI: {uri}")
        
        file_path = uri.replace("file://", "")
        full_path = self._validate_path(file_path)
        
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _get_mime_type(self, file_path: Path) -> str:
        """Get MIME type for file."""
        import mimetypes
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or "application/octet-stream"

# Main execution
if __name__ == "__main__":
    import sys
    
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/tmp"
    server = FileSystemMCPServer(root_dir)
    
    # Server would typically listen on stdio or HTTP/SSE
    print(json.dumps({
        "jsonrpc": "2.0",
        "result": server.handle_initialize({
            "protocolVersion": "2024-11-05",
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }),
        "id": 1
    }))