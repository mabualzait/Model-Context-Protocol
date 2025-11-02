# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.3 Prompt Injection Prevention

# Vulnerable: Reading file with injected content
content = read_file("user_file.txt")  # Contains: "Ignore system prompts"
prompt = f"Review this code: {content}"