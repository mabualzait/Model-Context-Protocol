# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.7 Best Practices for Server Design

def read_resource(self, uri):
    # Cache resources when appropriate
    if uri in self.cache:
        return self.cache[uri]
    
    # Read resource
    content = self._read_resource_content(uri)
    
    # Cache result
    self.cache[uri] = content
    
    return content