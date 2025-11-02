# 📖 Chapter: Chapter 13: Multi-Agent Systems with MCP
# 📖 Section: 13.3 Workflow Coordination

class ParallelWorkflowCoordinator:
    """Coordinate parallel workflows across agents."""
    
    def __init__(self, orchestrator: MultiAgentOrchestrator):
        self.orchestrator = orchestrator
    
    async def execute_parallel_workflow(self, workflow: Dict) -> Dict:
        """Execute workflow where tasks can run in parallel."""
        tasks = workflow.get("tasks", [])
        initial_context = workflow.get("initial_context", {})
        
        # Execute all tasks in parallel
        task_coroutines = [
            self._execute_task_async(task, initial_context) 
            for task in tasks
        ]
        
        results = await asyncio.gather(*task_coroutines, return_exceptions=True)
        
        # Process results
        processed_results = []
        for task, result in zip(tasks, results):
            if isinstance(result, Exception):
                processed_results.append({
                    "task_id": task["id"],
                    "status": "error",
                    "error": str(result)
                })
            else:
                processed_results.append(result)
        
        # Check if all tasks succeeded
        all_succeeded = all(
            r.get("status") == "success" for r in processed_results
        )
        
        return {
            "status": "success" if all_succeeded else "partial_failure",
            "results": processed_results
        }
    
    async def _execute_task_async(self, task: Dict, context: Dict) -> Dict:
        """Execute task asynchronously."""
        # Substitute context
        task = self._substitute_context(task, context)
        
        # Select agent
        agent_id = self.orchestrator._select_agent_for_task(task)
        if not agent_id:
            return {"status": "error", "message": "No suitable agent"}
        
        # Execute in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self.orchestrator.assign_task,
            agent_id,
            task
        )
        
        return {
            "task_id": task["id"],
            "agent_id": agent_id,
            **result
        }
    
    def _substitute_context(self, task: Dict, context: Dict) -> Dict:
        """Substitute context variables in task."""
        import json
        import re
        
        task_str = json.dumps(task)
        
        for key, value in context.items():
            pattern = f'\\$\\{{{key}\\}}'
            task_str = re.sub(pattern, json.dumps(value), task_str)
        
        return json.loads(task_str)