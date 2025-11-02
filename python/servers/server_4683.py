# 📖 Chapter: Chapter 4: MCP Servers: Implementation and Design
# 📖 Section: 4.5 Prompts: Structured Prompt Templates

class CodeReviewPromptServer:
    def __init__(self):
        self.prompts = {
            "code_review": self._code_review_prompt,
            "documentation": self._documentation_prompt,
            "refactoring": self._refactoring_prompt
        }
    
    def list_prompts(self):
        """List available prompts"""
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
                        },
                        {
                            "name": "focus",
                            "description": "Focus area (security, performance, style)",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "documentation",
                    "description": "Generate documentation for code",
                    "arguments": [
                        {
                            "name": "code",
                            "description": "Code to document",
                            "required": True
                        }
                    ]
                },
                {
                    "name": "refactoring",
                    "description": "Suggest refactoring improvements",
                    "arguments": [
                        {
                            "name": "code",
                            "description": "Code to refactor",
                            "required": True
                        }
                    ]
                }
            ]
        }
    
    def get_prompt(self, name, arguments):
        """Get prompt with arguments"""
        if name not in self.prompts:
            raise ValueError(f"Unknown prompt: {name}")
        
        return self.prompts[name](arguments)
    
    def _code_review_prompt(self, args):
        code = args.get("code")
        focus = args.get("focus", "security")
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Review this code for {focus} issues:\n\n```python\n{code}\n```"
                    }
                }
            ]
        }
    
    def _documentation_prompt(self, args):
        code = args.get("code")
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Generate documentation for this code:\n\n```python\n{code}\n```"
                    }
                }
            ]
        }
    
    def _refactoring_prompt(self, args):
        code = args.get("code")
        
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Suggest refactoring improvements for this code:\n\n```python\n{code}\n```"
                    }
                }
            ]
        }