# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.4 Tools: Exposing Executable Functions

def list_tools(self):
    return {
        "tools": [
            {
                "name": "read_file",
                "description": "Read a file from the filesystem",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path to read"
                        }
                    },
                    "required": ["path"]
                }
            }
        ]
    }