# 📖 Chapter: Chapter 12: Compliance and Governance
# 📖 Section: 12.1 Data Protection Regulations

class CCPAComplianceManager:
    """Manage CCPA compliance for MCP systems."""
    
    def __init__(self):
        self.personal_information: Dict[str, Dict] = {}
        self.sale_of_data: Dict[str, List[Dict]] = {}  # user_id -> sales records
    
    def handle_consumer_request(self, user_id: str, request_type: str) -> Dict:
        """Handle CCPA consumer request."""
        if request_type == "know":
            return self._handle_know_request(user_id)
        elif request_type == "delete":
            return self._handle_delete_request(user_id)
        elif request_type == "opt_out":
            return self._handle_opt_out_request(user_id)
        else:
            return {"status": "error", "message": "Unknown request type"}
    
    def _handle_know_request(self, user_id: str) -> Dict:
        """Handle CCPA 'know' request."""
        personal_info = self.personal_information.get(user_id, {})
        sales_records = self.sale_of_data.get(user_id, [])
        
        return {
            "personal_information": personal_info,
            "categories_of_personal_information": list(personal_info.keys()),
            "sources": self._get_data_sources(user_id),
            "business_purposes": self._get_business_purposes(user_id),
            "sales_of_personal_information": sales_records
        }
    
    def _handle_delete_request(self, user_id: str) -> Dict:
        """Handle CCPA delete request."""
        if user_id in self.personal_information:
            del self.personal_information[user_id]
        
        if user_id in self.sale_of_data:
            del self.sale_of_data[user_id]
        
        return {"status": "success", "message": "Personal information deleted"}
    
    def _handle_opt_out_request(self, user_id: str) -> Dict:
        """Handle CCPA opt-out of sale request."""
        # Record opt-out
        if user_id not in self.sale_of_data:
            self.sale_of_data[user_id] = []
        
        self.sale_of_data[user_id].append({
            "action": "opt_out",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return {"status": "success", "message": "Opted out of sale of personal information"}
    
    def _get_data_sources(self, user_id: str) -> List[str]:
        """Get data sources for user."""
        # Implementation to retrieve data sources
        return ["direct_collection", "third_party"]
    
    def _get_business_purposes(self, user_id: str) -> List[str]:
        """Get business purposes for data processing."""
        # Implementation to retrieve business purposes
        return ["service_delivery", "security", "compliance"]