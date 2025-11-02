# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.3 Prompt Injection Prevention

import re
from typing import List

class PromptSanitizer:
    """Sanitize inputs to prevent prompt injection."""
    
    # Known injection patterns
    INJECTION_PATTERNS = [
        r"(?i)ignore\s+(previous|all|above|below)\s+(instructions|commands|prompts)",
        r"(?i)forget\s+(previous|all|everything)",
        r"(?i)system\s*:.*",
        r"(?i)assistant\s*:.*",
        r"(?i)user\s*:.*",
        r"<\|.*?\|>",  # Special tokens
    ]
    
    def sanitize(self, text: str) -> str:
        """Sanitize text to remove injection patterns."""
        sanitized = text
        
        for pattern in self.INJECTION_PATTERNS:
            sanitized = re.sub(pattern, "", sanitized)
        
        # Remove excessive whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        return sanitized
    
    def contains_injection(self, text: str) -> bool:
        """Check if text contains injection patterns."""
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, text):
                return True
        return False
    
    def validate_and_sanitize(self, text: str) -> str:
        """Validate and sanitize text."""
        if self.contains_injection(text):
            # Log potential injection attempt
            self._log_injection_attempt(text)
            # Sanitize and return
            return self.sanitize(text)
        
        return text
    
    def _log_injection_attempt(self, text: str):
        """Log injection attempt for security monitoring."""
        # Implementation for logging
        pass