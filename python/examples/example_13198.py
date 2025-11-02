# 📖 Chapter: Chapter 9: Advanced MCP Patterns
# 📖 Section: 9.5 Complex Workflow Orchestration

class MCPWorkflowEngine:
    """Engine for orchestrating complex MCP workflows."""
    
    def __init__(self, multi_client: MultiServerMCPClient):
        self.multi_client = multi_client
        self.workflows: Dict[str, Dict] = {}
        self.workflow_state: Dict[str, Dict] = {}
    
    def register_workflow(self, workflow_id: str, workflow_def: Dict):
        """Register a workflow definition."""
        self.workflows[workflow_id] = workflow_def
    
    async def execute_workflow(self, workflow_id: str, 
                              initial_context: Dict = None) -> Dict:
        """Execute a registered workflow."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        context = initial_context or {}
        execution_log = []
        
        steps = workflow.get('steps', [])
        
        for step in steps:
            step_id = step['id']
            step_type = step['type']
            
            try:
                if step_type == 'parallel':
                    result = await self._execute_parallel_step(step, context)
                elif step_type == 'conditional':
                    result = await self._execute_conditional_step(step, context)
                elif step_type == 'loop':
                    result = await self._execute_loop_step(step, context)
                else:
                    result = await self._execute_simple_step(step, context)
                
                context[step_id] = result
                execution_log.append({
                    'step_id': step_id,
                    'status': 'success',
                    'result': result
                })
                
            except Exception as e:
                execution_log.append({
                    'step_id': step_id,
                    'status': 'error',
                    'error': str(e)
                })
                
                if workflow.get('stop_on_error', True):
                    break
        
        return {
            'workflow_id': workflow_id,
            'status': 'completed' if all(log['status'] == 'success' for log in execution_log) else 'failed',
            'execution_log': execution_log,
            'final_context': context
        }
    
    async def _execute_simple_step(self, step: Dict, context: Dict) -> Dict:
        """Execute a simple workflow step."""
        server_id = step['server_id']
        operation = step['operation']
        params = self._substitute_context(step.get('params', {}), context)
        
        if operation == 'call_tool':
            return await self.multi_client.call_tool_async(
                server_id, step['tool_name'], params
            )
        elif operation == 'read_resource':
            return await self.multi_client.servers[server_id].read_resource(
                step['resource_uri']
            )
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    async def _execute_parallel_step(self, step: Dict, context: Dict) -> Dict:
        """Execute parallel workflow steps."""
        parallel_steps = step.get('steps', [])
        
        tasks = [
            self._execute_simple_step(sub_step, context)
            for sub_step in parallel_steps
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            'results': [
                r if not isinstance(r, Exception) else {'error': str(r)}
                for r in results
            ]
        }
    
    async def _execute_conditional_step(self, step: Dict, context: Dict) -> Dict:
        """Execute conditional workflow step."""
        condition = step.get('condition', '')
        then_step = step.get('then')
        else_step = step.get('else')
        
        # Evaluate condition
        condition_met = self._evaluate_condition(condition, context)
        
        if condition_met and then_step:
            return await self._execute_simple_step(then_step, context)
        elif not condition_met and else_step:
            return await self._execute_simple_step(else_step, context)
        
        return {'skipped': True}
    
    async def _execute_loop_step(self, step: Dict, context: Dict) -> Dict:
        """Execute loop workflow step."""
        loop_var = step.get('loop_variable')
        items = step.get('items', [])
        body_step = step['body']
        
        results = []
        
        for item in items:
            context[loop_var] = item
            result = await self._execute_simple_step(body_step, context)
            results.append(result)
        
        return {'results': results}
    
    def _evaluate_condition(self, condition: str, context: Dict) -> bool:
        """Evaluate workflow condition."""
        # Simplified condition evaluation
        # In production, use proper expression evaluator
        try:
            # Replace context variables
            for key, value in context.items():
                condition = condition.replace(f'${{{key}}}', str(value))
            
            return eval(condition)
        except:
            return False
    
    def _substitute_context(self, params: Dict, context: Dict) -> Dict:
        """Substitute context variables in parameters."""
        import json
        import re
        
        params_str = json.dumps(params)
        
        for key, value in context.items():
            pattern = f'\\$\\{{{key}\\}}'
            params_str = re.sub(pattern, json.dumps(value), params_str)
        
        return json.loads(params_str)