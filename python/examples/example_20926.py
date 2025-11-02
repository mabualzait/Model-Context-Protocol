# 📖 Chapter: Appendices
# 📖 Section: E.1 Common MCP Patterns

# List all resources
resources = client.list_resources()
for resource in resources:
    print(f"{resource['uri']}: {resource['name']}")

# Read specific resource
content = client.read_resource("file:///path/to/file.txt")

# Subscribe to resource updates
client.subscribe_resource("file:///path/to/file.txt")