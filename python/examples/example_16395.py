# 📖 Chapter: Chapter 13: Multi-Agent Systems with MCP
# 📖 Section: 13.1 Orchestrating Multiple AI Agents

class AgentLoadBalancer:
    """Load balancer for distributing tasks across agents."""
    
    def __init__(self, orchestrator: MultiAgentOrchestrator):
        self.orchestrator = orchestrator
        self.agent_metrics: Dict[str, Dict] = {}
    
    def select_best_agent(self, task: Dict) -> Optional[str]:
        """Select best agent for task based on load and capability."""
        required_capabilities = task.get("required_capabilities", [])
        suitable_agents = []
        
        for agent_id, agent in self.orchestrator.agents.items():
            if agent["status"] != "available":
                continue
            
            agent_capabilities = set(agent["capabilities"])
            required_set = set(required_capabilities)
            
            if required_set.issubset(agent_capabilities):
                metrics = self.agent_metrics.get(agent_id, {
                    "tasks_completed": 0,
                    "avg_duration": 0,
                    "current_load": 0
                })
                suitable_agents.append({
                    "agent_id": agent_id,
                    "metrics": metrics
                })
        
        if not suitable_agents:
            return None
        
        # Select agent with lowest load
        best_agent = min(suitable_agents, key=lambda x: x["metrics"]["current_load"])
        return best_agent["agent_id"]
    
    def update_metrics(self, agent_id: str, task_duration: float):
        """Update agent metrics after task completion."""
        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = {
                "tasks_completed": 0,
                "avg_duration": 0,
                "current_load": 0
            }
        
        metrics = self.agent_metrics[agent_id]
        metrics["tasks_completed"] += 1
        
        # Update average duration
        total = metrics["tasks_completed"]
        metrics["avg_duration"] = (
            (metrics["avg_duration"] * (total - 1) + task_duration) / total
        )
        
        # Update current load (simplified)
        metrics["current_load"] = metrics["avg_duration"] * metrics["tasks_completed"]