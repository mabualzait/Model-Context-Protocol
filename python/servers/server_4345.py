# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.3 Resources: Providing Data Access

def list_resources(self):
    return {
        "resources": [
            {
                "uri": "file:///path/to/file.txt",
                "name": "file.txt",
                "mimeType": "text/plain",
                "description": "A text file"
            }
        ]
    }