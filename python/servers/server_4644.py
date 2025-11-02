# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.5 Prompts: Structured Prompt Templates

def list_prompts(self):
    return {
        "prompts": [
            {
                "name": "code_review",
                "description": "Review code for security issues",
                "arguments": [
                    {
                        "name": "code",
                        "description": "Code to review",
                        "required": True
                    }
                ]
            }
        ]
    }