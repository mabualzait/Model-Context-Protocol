# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.5 Prompts: Structured Prompt Templates

def get_prompt(self, name, arguments):
    if name == "code_review":
        code = arguments.get("code")
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Review this code for security issues:\n\n```python\n{code}\n```"
                    }
                }
            ]
        }