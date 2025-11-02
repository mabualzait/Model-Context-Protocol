# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.4 Secure Data Handling

from enum import Enum
from typing import List

class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class DataClassifier:
    """Classify data by sensitivity."""
    
    def __init__(self):
        self.classification_rules = {
            DataClassification.RESTRICTED: [
                r"(?i)\b(ssn|social security|credit card|password|api key|secret)\b",
                r"\b[A-Z]{2}\d{6}\b",  # Example: SSN pattern
                r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",  # Credit card
            ],
            DataClassification.CONFIDENTIAL: [
                r"(?i)\b(email|phone|address|personal)\b",
            ],
            DataClassification.INTERNAL: [
                r"(?i)\b(internal|proprietary|company)\b",
            ]
        }
    
    def classify(self, text: str) -> DataClassification:
        """Classify text by sensitivity."""
        import re
        
        for classification in [DataClassification.RESTRICTED, 
                              DataClassification.CONFIDENTIAL,
                              DataClassification.INTERNAL]:
            for pattern in self.classification_rules.get(classification, []):
                if re.search(pattern, text):
                    return classification
        
        return DataClassification.PUBLIC