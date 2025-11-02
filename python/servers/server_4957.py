# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.7 Best Practices for Server Design

def call_tool(self, name, arguments):
    if not name:
        raise ValueError("Tool name is required")
    if not isinstance(arguments, dict):
        raise ValueError("Arguments must be a dictionary")
    # Validate specific arguments
    if "path" in arguments and not isinstance(arguments["path"], str):
        raise ValueError("Path must be a string")