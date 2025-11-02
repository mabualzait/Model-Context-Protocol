# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.1 Authentication and Authorization

from enum import Enum
from typing import List, Set

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    READONLY = "readonly"

class RBACAuthorizer:
    """Role-based access control."""
    
    def __init__(self):
        self.role_permissions = {
            Role.ADMIN: {"read", "write", "delete", "admin"},
            Role.USER: {"read", "write"},
            Role.READONLY: {"read"}
        }
    
    def check_permission(self, role: Role, action: str, resource: str) -> bool:
        """Check if role has permission for action."""
        permissions = self.role_permissions.get(role, set())
        
        # Check generic permission
        if action in permissions:
            return True
        
        # Check resource-specific permission
        resource_permission = f"{action}:{resource}"
        if resource_permission in permissions:
            return True
        
        return False