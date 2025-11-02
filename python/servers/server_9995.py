# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.5 Troubleshooting Common Issues

class DebugResourceListing:
    """Debug resource listing issues."""
    
    def debug_resource_listing(self, server: 'MCPServer'):
        """Debug why resources aren't listed."""
        # Check if resource handler is registered
        if not hasattr(server, 'on_list_resources'):
            print("ERROR: Resource handler not registered")
            return
        
        # Check if resources exist
        resources = server.list_resources()
        print(f"Found {len(resources)} resources")
        
        # Check each resource
        for resource in resources:
            print(f"Resource URI: {resource.uri}")
            print(f"Resource Name: {resource.name}")
            print(f"Resource MIME Type: {resource.mimeType}")
            
            # Try to read resource
            try:
                content = server.read_resource(resource.uri)
                print(f"✓ Resource readable ({len(content)} bytes)")
            except Exception as e:
                print(f"✗ Error reading resource: {e}")