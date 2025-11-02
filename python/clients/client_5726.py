# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.2 Connection Management and Session Handling

class MCPSession:
    def __init__(self):
        self.server_capabilities = {}
        self.server_info = {}
        self.resources = {}
        self.tools = {}
        self.prompts = {}
        self.subscriptions = {}
    
    def update_capabilities(self, capabilities):
        """Update server capabilities"""
        self.server_capabilities = capabilities
    
    def add_resource(self, resource):
        """Add discovered resource"""
        self.resources[resource["uri"]] = resource
    
    def add_tool(self, tool):
        """Add discovered tool"""
        self.tools[tool["name"]] = tool
    
    def add_prompt(self, prompt):
        """Add discovered prompt"""
        self.prompts[prompt["name"]] = prompt