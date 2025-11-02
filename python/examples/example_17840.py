# 📖 Chapter: Chapter 14: MCP and Enterprise Integration
# 📖 Section: 14.3 Enterprise Patterns and Anti-Patterns

class EnterpriseGatewayAggregation:
    """Aggregate multiple enterprise services through MCP gateway."""
    
    def __init__(self):
        self.backend_services: Dict[str, 'MCPClient'] = {}
        self.aggregation_rules: Dict[str, List[str]] = {}
    
    def register_backend_service(self, service_id: str, 
                                client: 'MCPClient'):
        """Register backend service."""
        self.backend_services[service_id] = client
    
    def define_aggregation(self, aggregation_id: str, 
                          service_ids: List[str]):
        """Define aggregation of multiple services."""
        self.aggregation_rules[aggregation_id] = service_ids
    
    def aggregate_resources(self, aggregation_id: str) -> Dict:
        """Aggregate resources from multiple services."""
        service_ids = self.aggregation_rules.get(aggregation_id, [])
        
        all_resources = {}
        for service_id in service_ids:
            if service_id in self.backend_services:
                client = self.backend_services[service_id]
                try:
                    resources = client.list_resources()
                    all_resources[service_id] = resources
                except Exception as e:
                    print(f"Error aggregating from {service_id}: {e}")
        
        return all_resources