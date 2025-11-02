# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.6 Advanced Integration Patterns

class PluginMCPServer:
    """MCP server that acts as a plugin system."""
    
    def __init__(self, app_context: Dict):
        self.app_context = app_context
        self.plugins: Dict[str, 'Plugin'] = {}
        self.server = MCPServer(
            name="plugin-server",
            version="1.0.0"
        )
        self._register_handlers()
    
    def register_plugin(self, plugin_id: str, plugin: 'Plugin'):
        """Register a plugin."""
        self.plugins[plugin_id] = plugin
        
        # Expose plugin as MCP tool
        self.server.register_tool({
            "name": f"plugin_{plugin_id}",
            "description": plugin.description,
            "inputSchema": plugin.schema
        })
    
    def _register_handlers(self):
        """Register MCP handlers."""
        self.server.on_call_tool = self._handle_tool_call
    
    def _handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        """Handle tool call - route to plugin."""
        if name.startswith("plugin_"):
            plugin_id = name.replace("plugin_", "")
            
            if plugin_id not in self.plugins:
                raise ValueError(f"Plugin not found: {plugin_id}")
            
            plugin = self.plugins[plugin_id]
            result = plugin.execute(arguments, self.app_context)
            
            return {
                "content": [{"type": "text", "text": json.dumps(result)}]
            }
        
        raise ValueError(f"Unknown tool: {name}")

class Plugin:
    """Base plugin interface."""
    
    def __init__(self, plugin_id: str, description: str, schema: Dict):
        self.plugin_id = plugin_id
        self.description = description
        self.schema = schema
    
    def execute(self, arguments: Dict, context: Dict) -> Dict:
        """Execute plugin with arguments and context."""
        raise NotImplementedError()