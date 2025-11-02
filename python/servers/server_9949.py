# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.5 Troubleshooting Common Issues

# Check server logs
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable verbose logging
server = SimpleMCPServer(debug=True)

# Check configuration
import json
with open("config.json") as f:
    config = json.load(f)
    print(f"Configuration: {json.dumps(config, indent=2)}")