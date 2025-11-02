# 📖 Chapter: Chapter 12: Compliance and Governance
# 📖 Section: 12.1 Data Protection Regulations

class DataMinimizationManager:
    """Enforce data minimization and purpose limitation."""
    
    def __init__(self):
        self.allowed_purposes: Dict[str, List[str]] = {}  # user_id -> purposes
        self.data_retention_policies: Dict[str, int] = {}  # data_type -> days
    
    def validate_data_collection(self, user_id: str, data: Dict, purpose: str) -> bool:
        """Validate data collection against purpose limitation."""
        allowed_purposes = self.allowed_purposes.get(user_id, [])
        
        if purpose not in allowed_purposes:
            return False
        
        # Check if data is necessary for purpose
        if not self._is_data_necessary(data, purpose):
            return False
        
        return True
    
    def _is_data_necessary(self, data: Dict, purpose: str) -> bool:
        """Check if data is necessary for purpose."""
        # Purpose-specific data requirements
        purpose_requirements = {
            "authentication": ["user_id", "password_hash"],
            "analytics": ["user_id", "action"],
            "personalization": ["user_id", "preferences"]
        }
        
        required_fields = purpose_requirements.get(purpose, [])
        
        # Check if all required fields are present and no unnecessary fields
        data_fields = set(data.keys())
        required_set = set(required_fields)
        
        # Must have required fields
        if not required_set.issubset(data_fields):
            return False
        
        # Should not have excessive fields
        excess_fields = data_fields - required_set
        if len(excess_fields) > len(required_fields):
            return False  # Too much unnecessary data
        
        return True