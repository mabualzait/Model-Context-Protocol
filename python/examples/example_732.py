# 📖 Chapter: Chapter 1: Introduction to Model Context Protocol
# 📖 Section: 1.9 Detailed Use Cases and Implementation Examples

# 📁 File: python/servers/filesystem_server.py
# 📖 Chapter 1, Section 1.9: Use Case 1 - AI Code Assistant with File System Access
# 🔗 GitHub: https://github.com/mabualzait/Model-Context-Protocol/blob/main/python/servers/filesystem_server.py

# File System MCP Server
from pathlib import Path
from typing import Dict, List, Optional
import mimetypes

# Note: MCPServer, Resource, and Tool classes would be imported from your MCP SDK
# from mcp_sdk import MCPServer, Resource, Tool

class FileSystemMCPServer:
    """MCP server exposing file system operations."""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.server = MCPServer(name="filesystem", version="1.0.0")
        self._register_handlers()
    
    def _get_mime_type(self, file_path: Path) -> str:
        """Get MIME type for file."""
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or "application/octet-stream"
    
    def _register_handlers(self):
        """Register MCP handlers."""
        self.server.on_list_resources = self._list_resources
        self.server.on_read_resource = self._read_resource
        self.server.on_list_tools = self._list_tools
        self.server.on_call_tool = self._call_tool
    
    def _list_resources(self) -> List[Resource]:
        """List files as resources."""
        resources = []
        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                resources.append(Resource(
                    uri=f"file://{file_path}",
                    name=file_path.name,
                    mimeType=self._get_mime_type(file_path)
                ))
        return resources
    
    def _read_resource(self, uri: str) -> str:
        """Read file content."""
        path = Path(uri.replace("file://", ""))
        with open(path, 'r') as f:
            return f.read()
    
    def _list_tools(self) -> List[Tool]:
        """List file operations as tools."""
        return [
            Tool(
                name="read_file",
                description="Read file contents",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"}
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
            )
        ]
    
    def _call_tool(self, name: str, arguments: Dict) -> Dict:
        """Execute file operation."""
        if name == "read_file":
            path = Path(arguments["path"])
            with open(path, 'r') as f:
                content = f.read()
            return {"content": [{"type": "text", "text": content}]}
        elif name == "write_file":
            path = Path(arguments["path"])
            with open(path, 'w') as f:
                f.write(arguments["content"])
            return {"content": [{"type": "text", "text": "File written successfully"}]}
        else:
            raise ValueError(f"Unknown tool: {name}")