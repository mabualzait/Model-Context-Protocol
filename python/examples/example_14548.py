# 📖 Chapter: Chapter 11: Monitoring and Observability
# 📖 Section: 11.1 Logging Strategies

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class StructuredLogger:
    """Structured logging for MCP systems."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.INFO)
        
        # JSON formatter for structured logs
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log(self, level: LogLevel, message: str, **kwargs):
        """Log structured message."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.value,
            "service": self.service_name,
            "message": message,
            **kwargs
        }
        
        self.logger.log(getattr(logging, level.value), json.dumps(log_entry))
    
    def log_request(self, request_id: str, method: str, params: Dict, 
                   session_id: str = None):
        """Log MCP request."""
        self.log(
            LogLevel.INFO,
            "MCP request received",
            request_id=request_id,
            method=method,
            params=self._sanitize_params(params),
            session_id=session_id
        )
    
    def log_response(self, request_id: str, method: str, success: bool,
                    duration_ms: float, error: str = None):
        """Log MCP response."""
        self.log(
            LogLevel.INFO if success else LogLevel.ERROR,
            "MCP response sent",
            request_id=request_id,
            method=method,
            success=success,
            duration_ms=duration_ms,
            error=error
        )
    
    def log_session_event(self, session_id: str, event_type: str, 
                         details: Dict):
        """Log session event."""
        self.log(
            LogLevel.INFO,
            f"Session event: {event_type}",
            session_id=session_id,
            event_type=event_type,
            **details
        )
    
    def _sanitize_params(self, params: Dict) -> Dict:
        """Sanitize parameters for logging."""
        sensitive_keys = {"password", "api_key", "secret", "token", "key"}
        sanitized = {}
        
        for key, value in params.items():
            if key.lower() in sensitive_keys:
                sanitized[key] = "***MASKED***"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_params(value)
            else:
                sanitized[key] = value
        
        return sanitized