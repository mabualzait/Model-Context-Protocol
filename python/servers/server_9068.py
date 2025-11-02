# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.3 Implementing Tools

from pathlib import Path
from typing import Dict, Any
from mcp import Tool

class FileSystemTools:
    """File system tool implementation."""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
    
    def list_tools(self) -> List[Tool]:
        """List available tools."""
        return [
            Tool(
                name="read_file",
                description="Read contents of a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to file relative to root"
                        }
                    },
                    "required": ["path"]
                }
            ),
            Tool(
                name="write_file",
                description="Write content to a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to file relative to root"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write"
                        }
                    },
                    "required": ["path", "content"]
                }
            ),
            Tool(
                name="list_directory",
                description="List files in a directory",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path relative to root"
                        }
                    },
                    "required": ["path"]
                }
            )
        ]
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool."""
        if name == "read_file":
            return self._read_file(arguments)
        elif name == "write_file":
            return self._write_file(arguments)
        elif name == "list_directory":
            return self._list_directory(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    def _validate_path(self, path: str) -> Path:
        """Validate and resolve path."""
        full_path = (self.root_path / path).resolve()
        
        # Security check
        if not full_path.is_relative_to(self.root_path):
            raise PermissionError(f"Access denied: path outside root")
        
        return full_path
    
    def _read_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Read file tool."""
        path = self._validate_path(args["path"])
        
        if not path.exists():
            return {
                "content": [{"type": "text", "text": f"Error: File not found: {path}"}],
                "isError": True
            }
        
        if not path.is_file():
            return {
                "content": [{"type": "text", "text": f"Error: Not a file: {path}"}],
                "isError": True
            }
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                "content": [{"type": "text", "text": content}],
                "isError": False
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                "isError": True
            }
    
    def _write_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Write file tool."""
        path = self._validate_path(args["path"])
        content = args["content"]
        
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {
                "content": [{"type": "text", "text": f"Successfully wrote {len(content)} bytes to {path}"}],
                "isError": False
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                "isError": True
            }
    
    def _list_directory(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List directory tool."""
        path = self._validate_path(args["path"])
        
        if not path.exists():
            return {
                "content": [{"type": "text", "text": f"Error: Directory not found: {path}"}],
                "isError": True
            }
        
        if not path.is_dir():
            return {
                "content": [{"type": "text", "text": f"Error: Not a directory: {path}"}],
                "isError": True
            }
        
        try:
            items = []
            for item in sorted(path.iterdir()):
                item_type = "directory" if item.is_dir() else "file"
                size = item.stat().st_size if item.is_file() else 0
                items.append(f"{item_type:10s} {size:10d} {item.name}")
            
            result = "\n".join(items)
            return {
                "content": [{"type": "text", "text": result}],
                "isError": False
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                "isError": True
            }