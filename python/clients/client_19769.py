# 📖 Chapter: Appendices
# 📖 Section: A.2 Full MCP Client Implementation

#!/usr/bin/env python3
"""
Complete MCP Client Implementation
Full-featured MCP client with connection management, error handling, and retry logic.
"""

import json
import sys
import time
import uuid
from typing import Dict, List, Optional, Any
from enum import Enum
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class TransportType(Enum):
    STDIO = "stdio"
    HTTP = "http"
    SSE = "sse"

class MCPClient:
    """Complete MCP client implementation."""
    
    def __init__(self, endpoint: str, transport: TransportType = TransportType.STDIO):
        self.endpoint = endpoint
        self.transport = transport
        self.session_id: Optional[str] = None
        self.protocol_version = "2024-11-05"
        self.capabilities: Dict = {}
        self.server_info: Dict = {}
        self.message_id = 0
        self.request_timeout = 30
        self.max_retries = 3
        self.retry_delay = 1
        
        if transport == TransportType.HTTP:
            self.session = self._create_http_session()
    
    def _create_http_session(self):
        """Create HTTP session with retry strategy."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=self.retry_delay,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def connect(self):
        """Connect to MCP server."""
        if self.transport == TransportType.STDIO:
            # stdio transport would be handled by parent process
            self._initialize_stdio()
        elif self.transport == TransportType.HTTP:
            self._initialize_http()
        elif self.transport == TransportType.SSE:
            self._initialize_sse()
    
    def _initialize_stdio(self):
        """Initialize stdio transport."""
        # stdio is handled by parent process
        pass
    
    def _initialize_http(self):
        """Initialize HTTP transport."""
        request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": self.protocol_version,
                "capabilities": {},
                "clientInfo": {
                    "name": "mcp-client",
                    "version": "1.0.0"
                }
            },
            "id": self._next_message_id()
        }
        
        response = self._send_http_request(request)
        result = response.get("result", {})
        
        self.protocol_version = result.get("protocolVersion", self.protocol_version)
        self.capabilities = result.get("capabilities", {})
        self.server_info = result.get("serverInfo", {})
        
        # Send initialized notification
        self._send_notification("notifications/initialized", {})
    
    def _initialize_sse(self):
        """Initialize SSE transport."""
        # SSE implementation would go here
        pass
    
    def _send_http_request(self, request: Dict) -> Dict:
        """Send HTTP request."""
        try:
            response = self.session.post(
                self.endpoint,
                json=request,
                timeout=self.request_timeout,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"HTTP request failed: {e}")
    
    def _next_message_id(self) -> int:
        """Get next message ID."""
        self.message_id += 1
        return self.message_id
    
    def _send_notification(self, method: str, params: Dict):
        """Send notification (no response expected)."""
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        
        if self.transport == TransportType.HTTP:
            # HTTP doesn't support notifications directly
            # Would use WebSocket or similar
            pass
    
    def list_resources(self) -> List[Dict]:
        """List available resources."""
        request = {
            "jsonrpc": "2.0",
            "method": "resources/list",
            "params": {},
            "id": self._next_message_id()
        }
        
        response = self._send_request(request)
        return response.get("result", {}).get("resources", [])
    
    def read_resource(self, uri: str) -> str:
        """Read resource content."""
        request = {
            "jsonrpc": "2.0",
            "method": "resources/read",
            "params": {"uri": uri},
            "id": self._next_message_id()
        }
        
        response = self._send_request(request)
        contents = response.get("result", {}).get("contents", [])
        
        if contents:
            return contents[0].get("text", "")
        
        return ""
    
    def list_tools(self) -> List[Dict]:
        """List available tools."""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": self._next_message_id()
        }
        
        response = self._send_request(request)
        return response.get("result", {}).get("tools", [])
    
    def call_tool(self, name: str, arguments: Dict) -> Dict:
        """Call tool."""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            },
            "id": self._next_message_id()
        }
        
        response = self._send_request(request)
        return response.get("result", {})
    
    def _send_request(self, request: Dict) -> Dict:
        """Send request and handle response."""
        if self.transport == TransportType.HTTP:
            return self._send_http_request(request)
        elif self.transport == TransportType.STDIO:
            return self._send_stdio_request(request)
        else:
            raise ValueError(f"Unsupported transport: {self.transport}")
    
    def _send_stdio_request(self, request: Dict) -> Dict:
        """Send request via stdio."""
        # Write request to stdout
        request_json = json.dumps(request)
        print(request_json, file=sys.stdout)
        sys.stdout.flush()
        
        # Read response from stdin
        response_line = sys.stdin.readline()
        return json.loads(response_line)
    
    def disconnect(self):
        """Disconnect from server."""
        if hasattr(self, 'session'):
            self.session.close()

# Usage example
if __name__ == "__main__":
    client = MCPClient("http://localhost:8080", TransportType.HTTP)
    client.connect()
    
    resources = client.list_resources()
    print(f"Found {len(resources)} resources")
    
    tools = client.list_tools()
    print(f"Found {len(tools)} tools")
    
    if tools:
        result = client.call_tool(tools[0]["name"], {})
        print(f"Tool result: {result}")
    
    client.disconnect()