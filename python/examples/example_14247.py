# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.6 Audit Logging and Compliance

import json
import logging
from datetime import datetime
from typing import Dict, Any
from enum import Enum

class AuditEventType(Enum):
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    RESOURCE_ACCESS = "resource_access"
    TOOL_EXECUTION = "tool_execution"
    SECURITY_VIOLATION = "security_violation"
    CONFIGURATION_CHANGE = "configuration_change"

class AuditLogger:
    """Comprehensive audit logging."""
    
    def __init__(self, log_file: str):
        self.logger = logging.getLogger("mcp_audit")
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_event(self, event_type: AuditEventType, 
                  user_id: str, details: Dict[str, Any], 
                  success: bool = True):
        """Log audit event."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type.value,
            "user_id": user_id,
            "success": success,
            "details": details
        }
        
        self.logger.info(json.dumps(event))
    
    def log_authentication(self, user_id: str, method: str, success: bool, 
                          ip_address: str = None):
        """Log authentication event."""
        self.log_event(
            AuditEventType.AUTHENTICATION,
            user_id,
            {
                "method": method,
                "ip_address": ip_address
            },
            success
        )
    
    def log_resource_access(self, user_id: str, uri: str, action: str, success: bool):
        """Log resource access."""
        self.log_event(
            AuditEventType.RESOURCE_ACCESS,
            user_id,
            {
                "uri": uri,
                "action": action
            },
            success
        )
    
    def log_tool_execution(self, user_id: str, tool_name: str, arguments: Dict, 
                          success: bool, result_size: int = None):
        """Log tool execution."""
        # Mask sensitive arguments
        sanitized_args = self._mask_sensitive_args(arguments)
        
        self.log_event(
            AuditEventType.TOOL_EXECUTION,
            user_id,
            {
                "tool_name": tool_name,
                "arguments": sanitized_args,
                "result_size": result_size
            },
            success
        )
    
    def log_security_violation(self, user_id: str, violation_type: str, 
                              details: Dict):
        """Log security violation."""
        self.log_event(
            AuditEventType.SECURITY_VIOLATION,
            user_id,
            {
                "violation_type": violation_type,
                **details
            },
            success=False
        )
    
    def _mask_sensitive_args(self, args: Dict) -> Dict:
        """Mask sensitive arguments in logs."""
        sensitive_keys = {"password", "api_key", "secret", "token", "key"}
        masked = {}
        
        for key, value in args.items():
            if key.lower() in sensitive_keys:
                masked[key] = "***MASKED***"
            elif isinstance(value, dict):
                masked[key] = self._mask_sensitive_args(value)
            else:
                masked[key] = value
        
        return masked