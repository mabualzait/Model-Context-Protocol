# 📖 Chapter: Chapter 9: Advanced MCP Patterns
# 📖 Section: 9.1 Multi-Server Architectures

class ChainedMCPWorkflow:
    """Execute workflows across multiple chained servers."""
    
    def __init__(self, multi_client: MultiServerMCPClient):
        self.multi_client = multi_client
        self.workflow_cache: Dict[str, Dict] = {}
    
    def execute_chain(self, chain_definition: List[Dict]) -> Dict:
        """Execute a chain of operations across servers."""
        results = []
        context = {}
        
        for step in chain_definition:
            step_id = step['id']
            server_id = step['server_id']
            operation = step['operation']
            params = step.get('params', {})
            
            # Substitute context variables
            params = self._substitute_context(params, context)
            
            try:
                if operation == 'call_tool':
                    tool_name = step['tool_name']
                    result = self.multi_client.servers[server_id].call_tool(
                        tool_name, params
                    )
                elif operation == 'read_resource':
                    uri = step['resource_uri']
                    result = self.multi_client.servers[server_id].read_resource(uri)
                else:
                    result = {'error': f'Unknown operation: {operation}'}
                
                # Store result in context
                context[step_id] = result
                results.append({
                    'step_id': step_id,
                    'status': 'success',
                    'result': result
                })
                
            except Exception as e:
                results.append({
                    'step_id': step_id,
                    'status': 'error',
                    'error': str(e)
                })
                break  # Stop chain on error
        
        return {
            'chain_id': chain_definition[0].get('chain_id', 'default'),
            'steps': results,
            'final_context': context
        }
    
    def _substitute_context(self, params: Dict, context: Dict) -> Dict:
        """Substitute context variables in parameters."""
        import json
        import re
        
        params_str = json.dumps(params)
        
        for key, value in context.items():
            # Replace ${key} with JSON-serialized value
            pattern = f'\\$\\{{{key}\\}}'
            params_str = re.sub(pattern, json.dumps(value), params_str)
        
        return json.loads(params_str)