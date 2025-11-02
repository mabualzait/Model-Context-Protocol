# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.7 Advanced Server Patterns

class ComposedMCPServer:
    """MCP server composed of multiple components."""
    
    def __init__(self):
        self.resource_providers: List['ResourceProvider'] = []
        self.tool_providers: List['ToolProvider'] = []
        self.prompt_providers: List['PromptProvider'] = []
    
    def register_resource_provider(self, provider: 'ResourceProvider'):
        """Register resource provider."""
        self.resource_providers.append(provider)
    
    def register_tool_provider(self, provider: 'ToolProvider'):
        """Register tool provider."""
        self.tool_providers.append(provider)
    
    def list_resources(self) -> List[Resource]:
        """Aggregate resources from all providers."""
        all_resources = []
        
        for provider in self.resource_providers:
            try:
                resources = provider.list_resources()
                all_resources.extend(resources)
            except Exception as e:
                logger.error(f"Error listing resources from provider: {e}")
        
        return all_resources
    
    def list_tools(self) -> List[Tool]:
        """Aggregate tools from all providers."""
        all_tools = []
        
        for provider in self.tool_providers:
            try:
                tools = provider.list_tools()
                all_tools.extend(tools)
            except Exception as e:
                logger.error(f"Error listing tools from provider: {e}")
        
        return all_tools