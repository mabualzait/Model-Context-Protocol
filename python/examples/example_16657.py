# 📖 Chapter: Chapter 13: Multi-Agent Systems with MCP
# 📖 Section: 13.3 Workflow Coordination

class SequentialWorkflowCoordinator:
    """Coordinate sequential workflows across agents."""
    
    def __init__(self, orchestrator: MultiAgentOrchestrator):
        self.orchestrator = orchestrator
    
    def execute_sequential_workflow(self, workflow: Dict) -> Dict:
        """Execute workflow where tasks must complete sequentially."""
        tasks = workflow.get("tasks", [])
        results = []
        context = {}
        
        for task in tasks:
            # Wait for previous task to complete
            if results:
                previous_result = results[-1]
                if previous_result.get("status") != "success":
                    return {
                        "status": "failed",
                        "failed_at_task": task["id"],
                        "results": results,
                        "context": context
                    }
            
            # Substitute context variables in task
            task = self._substitute_context(task, context)
            
            # Execute current task
            task_result = self._execute_task(task)
            results.append(task_result)
            
            # Update context with result
            if task_result.get("status") == "success":
                context[task["id"]] = task_result.get("result", {})
            
            # Check if task succeeded
            if task_result.get("status") != "success":
                return {
                    "status": "failed",
                    "failed_at_task": task["id"],
                    "results": results,
                    "context": context
                }
        
        return {
            "status": "success",
            "results": results,
            "final_context": context
        }
    
    def _execute_task(self, task: Dict) -> Dict:
        """Execute individual task."""
        agent_id = self.orchestrator._select_agent_for_task(task)
        if not agent_id:
            return {"status": "error", "message": "No suitable agent"}
        
        return self.orchestrator.assign_task(agent_id, task)
    
    def _substitute_context(self, task: Dict, context: Dict) -> Dict:
        """Substitute context variables in task."""
        import json
        import re
        
        task_str = json.dumps(task)
        
        for key, value in context.items():
            pattern = f'\\$\\{{{key}\\}}'
            task_str = re.sub(pattern, json.dumps(value), task_str)
        
        return json.loads(task_str)