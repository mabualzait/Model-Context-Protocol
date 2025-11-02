# 📖 Chapter: Chapter 15: The Future of MCP
# 📖 Section: 15.2 Protocol Evolution and Roadmap

class MultiTenantMCPServer:
    """MCP server with multi-tenant support."""
    
    def __init__(self):
        self.tenants: Dict[str, Dict] = {}
        self.tenant_resources: Dict[str, Dict] = {}  # tenant_id -> resources
        self.tenant_tools: Dict[str, Dict] = {}  # tenant_id -> tools
    
    def register_tenant(self, tenant_id: str, config: Dict):
        """Register tenant."""
        self.tenants[tenant_id] = {
            "tenant_id": tenant_id,
            "config": config,
            "created_at": time.time()
        }
    
    def list_tenant_resources(self, tenant_id: str) -> List[Dict]:
        """List resources for specific tenant."""
        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        return self.tenant_resources.get(tenant_id, [])
    
    def list_tenant_tools(self, tenant_id: str) -> List[Dict]:
        """List tools for specific tenant."""
        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        return self.tenant_tools.get(tenant_id, [])