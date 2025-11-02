# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.7 Best Practices for Server Design

def call_tool(self, name, arguments):
    # Validate permissions
    if not self.has_permission(name):
        raise PermissionError(f"Permission denied for tool: {name}")
    
    # Sanitize inputs
    sanitized_args = self.sanitize_arguments(arguments)
    
    # Execute tool
    return self._execute_tool(name, sanitized_args)