# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.4 Secure Data Handling

import re

class DataMasker:
    """Mask sensitive data in outputs."""
    
    def mask_sensitive_data(self, text: str) -> str:
        """Mask sensitive information."""
        masked = text
        
        # Mask SSNs
        masked = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', 'XXX-XX-XXXX', masked)
        
        # Mask credit cards
        masked = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', 
                       'XXXX-XXXX-XXXX-XXXX', masked)
        
        # Mask emails (partial)
        masked = re.sub(r'\b([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b',
                       r'***@\2', masked)
        
        # Mask API keys
        masked = re.sub(r'\b(api[_-]?key|apikey|secret[_-]?key)\s*[:=]\s*([a-zA-Z0-9_-]+)',
                       r'\1: ***MASKED***', masked, flags=re.IGNORECASE)
        
        return masked