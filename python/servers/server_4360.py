# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.3 Resources: Providing Data Access

def read_resource(self, uri):
    # Parse URI
    if uri.startswith("file://"):
        path = uri[7:]  # Remove "file://" prefix
        with open(path, 'r') as f:
            content = f.read()
        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "text/plain",
                    "text": content
                }
            ]
        }