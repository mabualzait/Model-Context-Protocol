# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.5 Advanced Host Patterns

from typing import Callable, Dict, List
from queue import Queue
import threading

class EventDrivenMCPHost(MCPHost):
    """Host with event-driven architecture."""
    
    def __init__(self):
        super().__init__()
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.event_queue: Queue = Queue()
        self.event_processor_thread = None
        self.running = False
    
    def on(self, event: str, handler: Callable):
        """Register event handler."""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    def emit(self, event: str, *args, **kwargs):
        """Emit event to handlers."""
        handlers = self.event_handlers.get(event, [])
        for handler in handlers:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in event handler for {event}: {e}")
    
    def start_event_processing(self):
        """Start event processing thread."""
        self.running = True
        
        def process_events():
            while self.running:
                try:
                    event_data = self.event_queue.get(timeout=1)
                    self._process_event(event_data)
                    self.event_queue.task_done()
                except:
                    continue
        
        self.event_processor_thread = threading.Thread(target=process_events, daemon=True)
        self.event_processor_thread.start()
    
    def create_session(self, client_info: Dict, server_config: Dict) -> str:
        """Create session with event handling."""
        session_id = super().create_session(client_info, server_config)
        
        # Emit session created event
        self.emit("session.created", session_id, client_info)
        
        return session_id
    
    def route_message(self, session_id: str, message: Dict) -> Optional[Dict]:
        """Route message with event handling."""
        # Emit message received event
        self.emit("message.received", session_id, message)
        
        try:
            response = super().route_message(session_id, message)
            
            # Emit message processed event
            self.emit("message.processed", session_id, message, response)
            
            return response
        except Exception as e:
            # Emit message error event
            self.emit("message.error", session_id, message, e)
            raise
    
    def destroy_session(self, session_id: str):
        """Destroy session with event handling."""
        # Emit session destroyed event
        self.emit("session.destroyed", session_id)
        
        super().destroy_session(session_id)

# Example usage
host = EventDrivenMCPHost()

# Register event handlers
host.on("session.created", lambda sid, info: print(f"Session created: {sid}"))
host.on("message.received", lambda sid, msg: logger.info(f"Message received: {msg}"))
host.on("message.error", lambda sid, msg, err: logger.error(f"Message error: {err}"))

host.start_event_processing()