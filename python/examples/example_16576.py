# 📖 Chapter: Chapter 13: Multi-Agent Systems with MCP
# 📖 Section: 13.2 Agent-to-Agent Communication via MCP

class SharedStateManager:
    """Manage shared state between agents via MCP resources."""
    
    def __init__(self, orchestrator: MultiAgentOrchestrator):
        self.orchestrator = orchestrator
        self.shared_state: Dict[str, Dict] = {}  # state_id -> state_data
        self.state_locks: Dict[str, 'Lock'] = {}  # state_id -> lock
    
    def create_shared_state(self, state_id: str, initial_value: Dict,
                           access_policy: str = "read_write"):
        """Create shared state resource."""
        self.shared_state[state_id] = {
            "state_id": state_id,
            "value": initial_value,
            "access_policy": access_policy,
            "created_at": time.time(),
            "updated_at": time.time(),
            "version": 0
        }
        
        # Create lock for state
        self.state_locks[state_id] = Lock()
        
        # Register as MCP resource
        resource_uri = f"state://{state_id}"
        return resource_uri
    
    def read_shared_state(self, state_id: str, agent_id: str) -> Dict:
        """Read shared state."""
        if state_id not in self.shared_state:
            raise ValueError(f"State {state_id} not found")
        
        state = self.shared_state[state_id]
        
        # Check access policy
        if state["access_policy"] == "write_only":
            raise PermissionError(f"Agent {agent_id} cannot read state {state_id}")
        
        return {
            "state_id": state_id,
            "value": state["value"],
            "version": state["version"],
            "updated_at": state["updated_at"]
        }
    
    def update_shared_state(self, state_id: str, agent_id: str, 
                          updates: Dict, merge: bool = True) -> Dict:
        """Update shared state."""
        if state_id not in self.shared_state:
            raise ValueError(f"State {state_id} not found")
        
        with self.state_locks[state_id]:
            state = self.shared_state[state_id]
            
            # Check access policy
            if state["access_policy"] == "read_only":
                raise PermissionError(f"Agent {agent_id} cannot write to state {state_id}")
            
            # Update state
            if merge:
                state["value"].update(updates)
            else:
                state["value"] = updates
            
            state["version"] += 1
            state["updated_at"] = time.time()
            
            return {
                "state_id": state_id,
                "version": state["version"],
                "updated_at": state["updated_at"]
            }