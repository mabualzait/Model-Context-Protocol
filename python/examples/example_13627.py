# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.1 Authentication and Authorization

from typing import Dict, Any, Callable

class ABACAuthorizer:
    """Attribute-based access control."""
    
    def __init__(self):
        self.policies: List[Callable] = []
    
    def add_policy(self, policy: Callable[[Dict[str, Any]], bool]):
        """Add access control policy."""
        self.policies.append(policy)
    
    def check_access(self, subject: Dict[str, Any], resource: Dict[str, Any], action: str) -> bool:
        """Check access using policies."""
        context = {
            "subject": subject,
            "resource": resource,
            "action": action
        }
        
        # All policies must allow access
        for policy in self.policies:
            if not policy(context):
                return False
        
        return True

# Example policy
def office_hours_policy(context: Dict[str, Any]) -> bool:
    """Policy: Only allow access during office hours."""
    import datetime
    current_hour = datetime.datetime.now().hour
    return 9 <= current_hour < 17

# Example usage
authorizer = ABACAuthorizer()
authorizer.add_policy(office_hours_policy)