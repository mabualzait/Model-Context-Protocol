# 📖 Chapter: Chapter 14: MCP and Enterprise Integration
# 📖 Section: 14.3 Enterprise Patterns and Anti-Patterns

class ServiceMeshMCPIntegration:
    """Integrate MCP with service mesh (e.g., Istio, Linkerd)."""
    
    def __init__(self, mesh_config: Dict):
        self.mesh_config = mesh_config
        self.service_registry: Dict[str, Dict] = {}
        self.traffic_policies: Dict[str, Dict] = {}
    
    def register_service(self, service_name: str, mcp_endpoint: str,
                        capabilities: List[str], namespace: str = "default"):
        """Register MCP service in mesh."""
        self.service_registry[service_name] = {
            "name": service_name,
            "mcp_endpoint": mcp_endpoint,
            "capabilities": capabilities,
            "namespace": namespace,
            "mesh_enabled": True,
            "registered_at": time.time()
        }
    
    def configure_traffic_policy(self, service_name: str, policy: Dict):
        """Configure traffic policy for service."""
        # Policies: retries, timeouts, circuit breakers, load balancing
        self.traffic_policies[service_name] = policy
    
    def get_service_endpoint(self, service_name: str) -> str:
        """Get service endpoint with service mesh routing."""
        if service_name not in self.service_registry:
            raise ValueError(f"Service {service_name} not registered")
        
        service = self.service_registry[service_name]
        
        # In service mesh, use DNS-based service discovery
        # Format: service-name.namespace.svc.cluster.local
        namespace = service.get("namespace", "default")
        return f"{service_name}.{namespace}.svc.cluster.local"
    
    def apply_circuit_breaker(self, service_name: str, 
                             failure_threshold: int = 5):
        """Apply circuit breaker pattern to service."""
        policy = {
            "circuit_breaker": {
                "consecutive_failures": failure_threshold,
                "timeout": 30,  # seconds
                "half_open_max_calls": 3
            }
        }
        self.configure_traffic_policy(service_name, policy)