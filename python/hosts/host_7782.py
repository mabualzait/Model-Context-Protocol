# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.5 Complete Host Implementation Example

import json
import uuid
import threading
import time
from typing import Dict, List, Optional
from queue import Queue
import subprocess

class MCPHost:
    def __init__(self, config: Dict):
        self.config = config
        self.sessions: Dict[str, MCPSession] = {}
        self.lock = threading.Lock()
        self.metrics = {
            "sessions_created": 0,
            "sessions_destroyed": 0,
            "requests_routed": 0,
            "errors": 0
        }
    
    def create_session(self, client_info: Dict, server_configs: List[Dict]) -> str:
        """Create new MCP session with multiple servers"""
        session_id = str(uuid.uuid4())
        
        session = MCPSession(session_id, client_info, server_configs)
        session.initialize()
        
        with self.lock:
            self.sessions[session_id] = session
            self.metrics["sessions_created"] += 1
        
        return session_id
    
    def route_message(self, session_id: str, message: Dict) -> Optional[Dict]:
        """Route message through session"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        try:
            if message.get("id"):
                # Request
                response = session.route_request(message)
                self.metrics["requests_routed"] += 1
                return response
            else:
                # Notification
                session.route_notification(message)
                return None
        except Exception as e:
            self.metrics["errors"] += 1
            raise
    
    def get_session(self, session_id: str) -> Optional[MCPSession]:
        """Get session by ID"""
        with self.lock:
            return self.sessions.get(session_id)
    
    def destroy_session(self, session_id: str):
        """Destroy session"""
        with self.lock:
            session = self.sessions.pop(session_id, None)
            if session:
                session.cleanup()
                self.metrics["sessions_destroyed"] += 1
    
    def get_metrics(self) -> Dict:
        """Get host metrics"""
        with self.lock:
            active_sessions = len(self.sessions)
            return {
                **self.metrics,
                "active_sessions": active_sessions
            }

class MCPSession:
    def __init__(self, session_id: str, client_info: Dict, server_configs: List[Dict]):
        self.session_id = session_id
        self.client_info = client_info
        self.server_configs = server_configs
        self.server_connections: Dict[str, ServerConnection] = {}
        self.lock = threading.Lock()
    
    def initialize(self):
        """Initialize session with servers"""
        for server_config in self.server_configs:
            server_id = server_config.get("id", str(uuid.uuid4()))
            connection = self._create_connection(server_config)
            connection.initialize({
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": self.client_info
            })
            self.server_connections[server_id] = connection
    
    def route_request(self, request: Dict) -> Dict:
        """Route request to appropriate server"""
        method = request.get("method", "")
        server_id = request.get("params", {}).get("server_id")
        
        if server_id and server_id in self.server_connections:
            connection = self.server_connections[server_id]
        elif len(self.server_connections) == 1:
            connection = list(self.server_connections.values())[0]
        else:
            raise ValueError("Multiple servers available, server_id required")
        
        with self.lock:
            return connection.send_request(request)
    
    def route_notification(self, notification: Dict):
        """Route notification to appropriate server"""
        server_id = notification.get("params", {}).get("server_id")
        
        if server_id and server_id in self.server_connections:
            connection = self.server_connections[server_id]
        elif len(self.server_connections) == 1:
            connection = list(self.server_connections.values())[0]
        else:
            raise ValueError("Multiple servers available, server_id required")
        
        with self.lock:
            connection.send_notification(notification)
    
    def _create_connection(self, server_config: Dict) -> 'ServerConnection':
        """Create server connection"""
        transport = server_config.get("transport", "stdio")
        
        if transport == "stdio":
            return StdioServerConnection(server_config["command"])
        elif transport == "http":
            return HTTPServerConnection(server_config["url"])
        else:
            raise ValueError(f"Unknown transport: {transport}")
    
    def cleanup(self):
        """Clean up session"""
        for connection in self.server_connections.values():
            connection.close()

# Example usage
if __name__ == "__main__":
    config = {
        "session_timeout": 3600,
        "max_sessions": 100
    }
    
    host = MCPHost(config)
    
    # Create session
    client_info = {
        "name": "example-client",
        "version": "1.0.0"
    }
    
    server_configs = [
        {
            "id": "filesystem",
            "transport": "stdio",
            "command": ["python", "filesystem-server.py"]
        },
        {
            "id": "database",
            "transport": "http",
            "url": "https://database-server.example.com"
        }
    ]
    
    session_id = host.create_session(client_info, server_configs)
    print(f"Created session: {session_id}")
    
    # Route message
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {"server_id": "filesystem"}
    }
    
    response = host.route_message(session_id, request)
    print(f"Response: {response}")
    
    # Clean up
    host.destroy_session(session_id)