# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.7 Advanced Server Patterns

class StatefulMCPServer:
    """MCP server with state management."""
    
    def __init__(self):
        self.session_state: Dict[str, Dict] = {}  # session_id -> state
        self.global_state: Dict = {}
        self.state_lock = threading.Lock()
    
    def get_session_state(self, session_id: str) -> Dict:
        """Get state for session."""
        with self.state_lock:
            if session_id not in self.session_state:
                self.session_state[session_id] = {
                    "created_at": time.time(),
                    "last_accessed": time.time(),
                    "data": {}
                }
            
            self.session_state[session_id]["last_accessed"] = time.time()
            return self.session_state[session_id]
    
    def update_session_state(self, session_id: str, updates: Dict):
        """Update session state."""
        with self.state_lock:
            state = self.get_session_state(session_id)
            state["data"].update(updates)
    
    def cleanup_expired_sessions(self, max_age: int = 3600):
        """Clean up expired sessions."""
        current_time = time.time()
        
        with self.state_lock:
            expired_sessions = [
                session_id
                for session_id, state in self.session_state.items()
                if current_time - state["last_accessed"] > max_age
            ]
            
            for session_id in expired_sessions:
                del self.session_state[session_id]