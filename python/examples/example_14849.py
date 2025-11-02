# 📖 Chapter: Chapter 11: Monitoring and Observability
# 📖 Section: 11.3 Debugging Distributed MCP Systems

import uuid
from typing import Dict, Optional
from contextvars import ContextVar

class TraceContext:
    """Distributed tracing context."""
    
    trace_id: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)
    span_id: ContextVar[Optional[str]] = ContextVar('span_id', default=None)
    parent_span_id: ContextVar[Optional[str]] = ContextVar('parent_span_id', default=None)
    
    @classmethod
    def start_trace(cls) -> str:
        """Start new trace."""
        trace_id = str(uuid.uuid4())
        span_id = str(uuid.uuid4())
        
        cls.trace_id.set(trace_id)
        cls.span_id.set(span_id)
        
        return trace_id
    
    @classmethod
    def start_span(cls, parent_span_id: str = None) -> str:
        """Start new span."""
        if parent_span_id:
            cls.parent_span_id.set(parent_span_id)
        
        span_id = str(uuid.uuid4())
        cls.span_id.set(span_id)
        
        return span_id
    
    @classmethod
    def get_context(cls) -> Dict[str, Optional[str]]:
        """Get current trace context."""
        return {
            "trace_id": cls.trace_id.get(),
            "span_id": cls.span_id.get(),
            "parent_span_id": cls.parent_span_id.get()
        }
    
    @classmethod
    def set_context(cls, trace_id: str, span_id: str, parent_span_id: str = None):
        """Set trace context."""
        cls.trace_id.set(trace_id)
        cls.span_id.set(span_id)
        if parent_span_id:
            cls.parent_span_id.set(parent_span_id)

class TracedMCPServer:
    """MCP server with distributed tracing."""
    
    def __init__(self):
        self.trace_context = TraceContext()
        self.spans: Dict[str, Dict] = {}
    
    def handle_request(self, request: Dict) -> Dict:
        """Handle request with tracing."""
        # Extract or create trace context
        trace_id = request.get("params", {}).get("_trace_id")
        if not trace_id:
            trace_id = self.trace_context.start_trace()
        
        span_id = self.trace_context.start_span()
        
        # Add trace context to request
        request["params"]["_trace_id"] = trace_id
        request["params"]["_span_id"] = span_id
        
        # Record span start
        self._record_span_start(trace_id, span_id, request)
        
        try:
            response = self._process_request(request)
            
            # Record span end (success)
            self._record_span_end(trace_id, span_id, success=True)
            
            return response
        except Exception as e:
            # Record span end (error)
            self._record_span_end(trace_id, span_id, success=False, error=str(e))
            raise
    
    def _record_span_start(self, trace_id: str, span_id: str, request: Dict):
        """Record span start."""
        self.spans[span_id] = {
            "trace_id": trace_id,
            "span_id": span_id,
            "start_time": time.time(),
            "method": request.get("method"),
            "request_id": request.get("id")
        }
    
    def _record_span_end(self, trace_id: str, span_id: str, success: bool, error: str = None):
        """Record span end."""
        if span_id in self.spans:
            span = self.spans[span_id]
            span["duration"] = time.time() - span["start_time"]
            span["success"] = success
            if error:
                span["error"] = error