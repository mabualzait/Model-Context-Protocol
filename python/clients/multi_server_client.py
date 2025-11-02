# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.2 Managing Multiple Client Instances

from typing import Dict, List, Optional
import uuid
import threading

class MCPSession:
    def __init__(self, session_id: str, client_info: Dict, server_config: Dict):
        self.session_id = session_id
        self.client_info = client_info
        self.server_config = server_config
        self.client_connection = None
        self.server_connection = None
        self.state = {}
        self.lock = threading.Lock()
    
    def initialize(self):
        """Initialize session"""
        # Create server connection
        self.server_connection = self._create_server_connection()
        
        # Initialize server
        init_response = self.server_connection.initialize({
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": self.client_info
        })
        
        self.state["server_capabilities"] = init_response.get("capabilities", {})
        self.state["server_info"] = init_response.get("serverInfo", {})
        
        return init_response
    
    def route_request(self, request: Dict) -> Dict:
        """Route request from client to server"""
        with self.lock:
            # Add session context
            request["params"] = request.get("params", {})
            request["params"]["session_id"] = self.session_id
            
            # Route to server
            response = self.server_connection.send_request(request)
            
            return response
    
    def route_notification(self, notification: Dict):
        """Route notification from client to server"""
        with self.lock:
            # Add session context
            notification["params"] = notification.get("params", {})
            notification["params"]["session_id"] = self.session_id
            
            # Route to server
            self.server_connection.send_notification(notification)
    
    def _create_server_connection(self):
        """Create server connection based on config"""
        if self.server_config.get("transport") == "stdio":
            return StdioServerConnection(self.server_config["command"])
        elif self.server_config.get("transport") == "http":
            return HTTPServerConnection(self.server_config["url"])
        else:
            raise ValueError(f"Unknown transport: {self.server_config.get('transport')}")

class MCPHost:
    def __init__(self):
        self.sessions: Dict[str, MCPSession] = {}
        self.lock = threading.Lock()
    
    def create_session(self, client_info: Dict, server_config: Dict) -> str:
        """Create new MCP session"""
        session_id = str(uuid.uuid4())
        
        session = MCPSession(session_id, client_info, server_config)
        session.initialize()
        
        with self.lock:
            self.sessions[session_id] = session
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[MCPSession]:
        """Get session by ID"""
        with self.lock:
            return self.sessions.get(session_id)
    
    def route_message(self, session_id: str, message: Dict) -> Optional[Dict]:
        """Route message through session"""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        if message.get("id"):
            # Request (expects response)
            return session.route_request(message)
        else:
            # Notification (no response)
            session.route_notification(message)
            return None
    
    def destroy_session(self, session_id: str):
        """Destroy session"""
        with self.lock:
            session = self.sessions.pop(session_id, None)
            if session:
                session.cleanup()

# --- Additional code from line 7536 ---
# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.2 Managing Multiple Client Instances

from queue import Queue
import threading

class ServerConnectionPool:
    def __init__(self, server_config: Dict, pool_size: int = 10):
        self.server_config = server_config
        self.pool_size = pool_size
        self.available_connections = Queue(maxsize=pool_size)
        self.active_connections = set()
        self.lock = threading.Lock()
    
    def get_connection(self):
        """Get connection from pool"""
        try:
            # Try to get existing connection
            connection = self.available_connections.get_nowait()
            return connection
        except:
            # Create new connection if pool is not full
            with self.lock:
                if len(self.active_connections) < self.pool_size:
                    connection = self._create_connection()
                    self.active_connections.add(connection)
                    return connection
                else:
                    # Wait for available connection
                    return self.available_connections.get()
    
    def return_connection(self, connection):
        """Return connection to pool"""
        if connection.is_healthy():
            self.available_connections.put(connection)
        else:
            # Remove unhealthy connection
            with self.lock:
                self.active_connections.discard(connection)
                connection.close()
    
    def _create_connection(self):
        """Create new server connection"""
        if self.server_config.get("transport") == "stdio":
            return StdioServerConnection(self.server_config["command"])
        elif self.server_config.get("transport") == "http":
            return HTTPServerConnection(self.server_config["url"])
        else:
            raise ValueError(f"Unknown transport: {self.server_config.get('transport')}")