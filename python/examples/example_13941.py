# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.3 Prompt Injection Prevention

class OutputValidator:
    """Validate outputs to prevent injection propagation."""
    
    def __init__(self):
        self.sanitizer = PromptSanitizer()
    
    def validate_tool_result(self, tool_name: str, result: Dict) -> Dict:
        """Validate tool result before using in prompts."""
        content = result.get("content", [])
        
        validated_content = []
        for item in content:
            if item.get("type") == "text":
                text = item.get("text", "")
                if self.sanitizer.contains_injection(text):
                    # Log and sanitize
                    self._log_suspicious_output(tool_name, text)
                    text = self.sanitizer.sanitize(text)
                
                validated_content.append({
                    "type": "text",
                    "text": text
                })
            else:
                validated_content.append(item)
        
        result["content"] = validated_content
        return result
    
    def validate_resource_content(self, uri: str, content: str) -> str:
        """Validate resource content before using."""
        if self.sanitizer.contains_injection(content):
            self._log_suspicious_resource(uri)
            return self.sanitizer.sanitize(content)
        
        return content
    
    def _log_suspicious_output(self, tool_name: str, text: str):
        """Log suspicious output."""
        # Security logging implementation
        pass
    
    def _log_suspicious_resource(self, uri: str):
        """Log suspicious resource."""
        # Security logging implementation
        pass