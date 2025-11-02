# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.3 Resources: Providing Data Access

def subscribe_resource(self, uri):
    # Store subscription
    self.subscriptions[uri] = True
    
    # Send notifications when resource changes
    # (Implementation depends on resource type)