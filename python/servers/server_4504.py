# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.4 Tools: Exposing Executable Functions

import os
import shutil
from pathlib import Path

class FileSystemToolServer:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.tools = {
            "read_file": self._read_file,
            "write_file": self._write_file,
            "list_directory": self._list_directory,
            "delete_file": self._delete_file
        }
    
    def list_tools(self):
        """List available tools"""
        return {
            "tools": [
                {
                    "name": "read_file",
                    "description": "Read a file from the filesystem",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"}
                        },
                        "required": ["path"]
                    }
                },
                {
                    "name": "write_file",
                    "description": "Write content to a file",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "content": {"type": "string"}
                        },
                        "required": ["path", "content"]
                    }
                },
                {
                    "name": "list_directory",
                    "description": "List files in a directory",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"}
                        },
                        "required": ["path"]
                    }
                },
                {
                    "name": "delete_file",
                    "description": "Delete a file",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"}
                        },
                        "required": ["path"]
                    }
                }
            ]
        }
    
    def call_tool(self, name, arguments):
        """Execute tool"""
        if name not in self.tools:
            return {
                "content": [
                    {"type": "text", "text": f"Unknown tool: {name}"}
                ],
                "isError": True
            }
        
        try:
            result = self.tools[name](arguments)
            return {
                "content": [
                    {"type": "text", "text": result}
                ],
                "isError": False
            }
        except Exception as e:
            return {
                "content": [
                    {"type": "text", "text": f"Error: {str(e)}"}
                ],
                "isError": True
            }
    
    def _read_file(self, args):
        path = Path(self.root_path / args["path"])
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, 'r') as f:
            return f.read()
    
    def _write_file(self, args):
        path = Path(self.root_path / args["path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(args["content"])
        return f"Written {len(args['content'])} bytes to {path}"
    
    def _list_directory(self, args):
        path = Path(self.root_path / args["path"])
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
        if not path.is_dir():
            raise ValueError(f"Not a directory: {path}")
        
        files = []
        for item in path.iterdir():
            files.append({
                "name": item.name,
                "type": "file" if item.is_file() else "directory"
            })
        return str(files)
    
    def _delete_file(self, args):
        path = Path(self.root_path / args["path"])
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        return f"Deleted {path}"