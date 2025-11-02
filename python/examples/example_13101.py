# 📖 Chapter: Chapter 9: Advanced MCP Patterns
# 📖 Section: 9.4 Custom Protocol Extensions

class ExtendedMCPServer(MCPServer):
    """MCP server with custom protocol extensions."""
    
    def __init__(self):
        super().__init__()
        self.custom_methods: Dict[str, callable] = {}
        self.register_custom_methods()
    
    def register_custom_methods(self):
        """Register custom protocol methods."""
        self.custom_methods = {
            'custom/health_check': self._custom_health_check,
            'custom/metrics': self._custom_metrics,
            'custom/batch': self._custom_batch,
        }
    
    def handle_request(self, request: Dict) -> Dict:
        """Handle requests including custom methods."""
        method = request.get('method')
        
        # Check for custom method
        if method in self.custom_methods:
            handler = self.custom_methods[method]
            params = request.get('params', {})
            
            try:
                result = handler(params)
                return {
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'result': result
                }
            except Exception as e:
                return {
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'error': {
                        'code': -32603,
                        'message': str(e)
                    }
                }
        
        # Delegate to standard handler
        return super().handle_request(request)
    
    def _custom_health_check(self, params: Dict) -> Dict:
        """Custom health check endpoint."""
        return {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'uptime': self._get_uptime()
        }
    
    def _custom_metrics(self, params: Dict) -> Dict:
        """Custom metrics endpoint."""
        return {
            'requests_total': self._get_request_count(),
            'active_connections': self._get_active_connections(),
            'resource_count': len(self.list_resources()),
            'tool_count': len(self.list_tools())
        }
    
    def _custom_batch(self, params: Dict) -> Dict:
        """Custom batch operation endpoint."""
        operations = params.get('operations', [])
        results = []
        
        for op in operations:
            try:
                if op['type'] == 'read_resource':
                    result = self.read_resource(op['uri'])
                elif op['type'] == 'call_tool':
                    result = self.call_tool(op['tool'], op['arguments'])
                else:
                    result = {'error': 'Unknown operation type'}
                
                results.append({
                    'operation_id': op.get('id'),
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                results.append({
                    'operation_id': op.get('id'),
                    'status': 'error',
                    'error': str(e)
                })
        
        return {'results': results}