# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.7 Best Practices for Server Design

def __init__(self):
    self.connections = {}
    
def cleanup(self):
    for conn in self.connections.values():
        conn.close()
    self.connections.clear()