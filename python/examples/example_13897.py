# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.3 Prompt Injection Prevention

class SecurePromptBuilder:
    """Build secure prompts with clear boundaries."""
    
    SYSTEM_BOUNDARY = "<|system|>"
    USER_BOUNDARY = "<|user|>"
    ASSISTANT_BOUNDARY = "<|assistant|>"
    
    def build_prompt(self, system_prompt: str, user_input: str, context: List[str] = None) -> str:
        """Build secure prompt with boundaries."""
        # Sanitize inputs
        sanitizer = PromptSanitizer()
        system_prompt = sanitizer.validate_and_sanitize(system_prompt)
        user_input = sanitizer.validate_and_sanitize(user_input)
        
        # Build prompt with clear boundaries
        prompt_parts = [
            self.SYSTEM_BOUNDARY,
            system_prompt,
            self.SYSTEM_BOUNDARY,
            "\n\n",
        ]
        
        # Add context if provided
        if context:
            prompt_parts.append("<|context|>\n")
            for ctx in context:
                sanitized_ctx = sanitizer.validate_and_sanitize(ctx)
                prompt_parts.append(f"- {sanitized_ctx}\n")
            prompt_parts.append("<|context|>\n\n")
        
        prompt_parts.extend([
            self.USER_BOUNDARY,
            user_input,
            self.USER_BOUNDARY,
            "\n\n",
            self.ASSISTANT_BOUNDARY
        ])
        
        return "".join(prompt_parts)