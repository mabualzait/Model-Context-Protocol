# 📖 Chapter: Appendices
# 📖 Section: E.1 Common MCP Patterns

# Check for errors in responses
response = client.call_tool("tool_name", {})
if response.get("isError"):
    error_text = response["content"][0]["text"]
    # Handle error
else:
    result_text = response["content"][0]["text"]
    # Process result

# Retry logic
import time
max_retries = 3
for attempt in range(max_retries):
    try:
        result = client.call_tool("tool_name", {})
        break
    except Exception as e:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            raise