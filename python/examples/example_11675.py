# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.6 Advanced Integration Patterns

class MicroservicesMCPGateway:
    """MCP gateway for microservices architecture."""
    
    def __init__(self):
        self.services: Dict[str, 'Microservice'] = {}
        self.server = MCPServer(
            name="microservices-gateway",
            version="1.0.0"
        )
        self._register_handlers()
    
    def register_service(self, service_name: str, service: 'Microservice'):
        """Register a microservice."""
        self.services[service_name] = service
        
        # Expose service endpoints as MCP tools
        for endpoint in service.endpoints:
            tool_name = f"{service_name}_{endpoint.name}"
            self.server.register_tool({
                "name": tool_name,
                "description": endpoint.description,
                "inputSchema": endpoint.schema
            })
    
    def _handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        """Handle tool call - route to microservice."""
        service_name, endpoint_name = name.split("_", 1)
        
        if service_name not in self.services:
            raise ValueError(f"Service not found: {service_name}")
        
        service = self.services[service_name]
        endpoint = service.get_endpoint(endpoint_name)
        
        # Call microservice endpoint
        result = endpoint.invoke(arguments)
        
        return {
            "content": [{"type": "text", "text": json.dumps(result)}]
        }