# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.3 Prompt Injection Prevention

# Vulnerable: Tool output directly in prompt
result = call_tool("web_search", {"query": user_query})
prompt = f"Summarize: {result}"  # Result might contain injections