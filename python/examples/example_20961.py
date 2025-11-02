# 📖 Chapter: Appendices
# 📖 Section: E.1 Common MCP Patterns

# List available prompts
prompts = client.list_prompts()

# Get prompt with arguments
prompt = client.get_prompt("analyze_document", {
    "document_path": "/path/to/doc.txt"
})

# Use prompt in AI interaction
messages = prompt["messages"]
for message in messages:
    print(f"{message['role']}: {message['content']['text']}")