# 📖 Chapter: Chapter 13: Multi-Agent Systems with MCP
# 📖 Section: 13.1 Orchestrating Multiple AI Agents

from typing import Dict, List, Optional
from enum import Enum
import asyncio
import time

class AgentRole(Enum):
    COORDINATOR = "coordinator"
    EXECUTOR = "executor"
    ANALYZER = "analyzer"
    VALIDATOR = "validator"

class MultiAgentOrchestrator:
    """Orchestrate multiple AI agents using MCP."""
    
    def __init__(self):
        self.agents: Dict[str, Dict] = {}
        self.agent_connections: Dict[str, 'MCPClient'] = {}
        self.workflows: Dict[str, List[Dict]] = {}
    
    def register_agent(self, agent_id: str, role: AgentRole, 
                       mcp_server_endpoint: str, capabilities: List[str]):
        """Register an agent with the orchestrator."""
        self.agents[agent_id] = {
            "agent_id": agent_id,
            "role": role.value,
            "mcp_server_endpoint": mcp_server_endpoint,
            "capabilities": capabilities,
            "status": "available",
            "registered_at": time.time()
        }
        
        # Connect to agent's MCP server
        client = MCPClient(mcp_server_endpoint)
        self.agent_connections[agent_id] = client
    
    def assign_task(self, agent_id: str, task: Dict) -> Dict:
        """Assign task to specific agent."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not registered")
        
        agent = self.agents[agent_id]
        if agent["status"] != "available":
            return {"status": "error", "message": "Agent not available"}
        
        # Update agent status
        agent["status"] = "busy"
        
        # Execute task via MCP
        client = self.agent_connections[agent_id]
        try:
            result = client.call_tool("execute_task", {"task": task})
            
            # Update agent status
            agent["status"] = "available"
            
            return {
                "status": "success",
                "agent_id": agent_id,
                "result": result
            }
        except Exception as e:
            agent["status"] = "available"
            return {"status": "error", "message": str(e)}
    
    def coordinate_workflow(self, workflow_id: str, tasks: List[Dict]) -> Dict:
        """Coordinate workflow across multiple agents."""
        workflow_result = {
            "workflow_id": workflow_id,
            "tasks": [],
            "overall_status": "pending",
            "start_time": time.time()
        }
        
        # Assign tasks to appropriate agents
        for task in tasks:
            # Select agent based on task requirements
            agent_id = self._select_agent_for_task(task)
            
            if not agent_id:
                workflow_result["overall_status"] = "error"
                workflow_result["error"] = f"No suitable agent for task: {task['id']}"
                break
            
            # Assign and execute task
            task_result = self.assign_task(agent_id, task)
            
            workflow_result["tasks"].append({
                "task_id": task["id"],
                "agent_id": agent_id,
                "status": task_result["status"],
                "result": task_result.get("result")
            })
            
            # Check if workflow should continue
            if task_result["status"] != "success":
                workflow_result["overall_status"] = "failed"
                break
        
        if workflow_result["overall_status"] == "pending":
            workflow_result["overall_status"] = "completed"
        
        workflow_result["duration"] = time.time() - workflow_result["start_time"]
        
        self.workflows[workflow_id] = workflow_result
        
        return workflow_result
    
    def _select_agent_for_task(self, task: Dict) -> Optional[str]:
        """Select appropriate agent for task."""
        required_capabilities = task.get("required_capabilities", [])
        
        # Find agents with required capabilities
        suitable_agents = []
        for agent_id, agent in self.agents.items():
            if agent["status"] != "available":
                continue
            
            agent_capabilities = set(agent["capabilities"])
            required_set = set(required_capabilities)
            
            if required_set.issubset(agent_capabilities):
                suitable_agents.append(agent_id)
        
        if not suitable_agents:
            return None
        
        # Select agent based on load balancing or priority
        return suitable_agents[0]