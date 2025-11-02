# 📖 Chapter: Chapter 13: Multi-Agent Systems with MCP
# 📖 Section: 13.4 Resource Sharing and Isolation

class ResourceIsolationManager:
    """Manage resource isolation between agents."""
    
    def __init__(self):
        self.agent_resources: Dict[str, set] = {}  # agent_id -> resource_uris
        self.shared_resources: set = set()
        self.resource_locks: Dict[str, str] = {}  # resource_uri -> agent_id
        self.isolation_policies: Dict[str, str] = {}  # agent_id -> policy
    
    def allocate_resource(self, agent_id: str, resource_uri: str, 
                        shared: bool = False, exclusive: bool = False) -> bool:
        """Allocate resource to agent."""
        # Check if resource is already allocated exclusively
        if resource_uri in self.resource_locks:
            lock_holder = self.resource_locks[resource_uri]
            if lock_holder != agent_id and exclusive:
                return False  # Resource locked by another agent
        
        # Check if resource is shared
        if resource_uri in self.shared_resources and exclusive:
            return False  # Cannot exclusively lock shared resource
        
        # Allocate resource
        if agent_id not in self.agent_resources:
            self.agent_resources[agent_id] = set()
        
        self.agent_resources[agent_id].add(resource_uri)
        
        if shared:
            self.shared_resources.add(resource_uri)
        else:
            # Exclusive lock
            self.resource_locks[resource_uri] = agent_id
        
        return True
    
    def release_resource(self, agent_id: str, resource_uri: str):
        """Release resource from agent."""
        if agent_id in self.agent_resources:
            self.agent_resources[agent_id].discard(resource_uri)
        
        if resource_uri in self.resource_locks:
            if self.resource_locks[resource_uri] == agent_id:
                del self.resource_locks[resource_uri]
        
        self.shared_resources.discard(resource_uri)
    
    def check_resource_access(self, agent_id: str, resource_uri: str) -> bool:
        """Check if agent has access to resource."""
        # Check if resource is shared
        if resource_uri in self.shared_resources:
            return True
        
        # Check if agent owns resource
        if agent_id in self.agent_resources:
            if resource_uri in self.agent_resources[agent_id]:
                return True
        
        return False
    
    def set_isolation_policy(self, agent_id: str, policy: str):
        """Set isolation policy for agent."""
        # Policies: "strict", "moderate", "relaxed"
        self.isolation_policies[agent_id] = policy