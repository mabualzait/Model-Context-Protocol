# 📖 Chapter: Chapter 12: Compliance and Governance
# 📖 Section: 12.1 Data Protection Regulations

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum

class DataSubjectRight(Enum):
    ACCESS = "access"
    RECTIFICATION = "rectification"
    ERASURE = "erasure"
    RESTRICTION = "restriction"
    PORTABILITY = "portability"
    OBJECTION = "objection"

class GDPRComplianceManager:
    """Manage GDPR compliance for MCP systems."""
    
    def __init__(self):
        self.user_data: Dict[str, Dict] = {}  # user_id -> data
        self.user_consent: Dict[str, Dict] = {}  # user_id -> consent records
        self.data_processing_logs: List[Dict] = []
    
    def handle_data_subject_request(self, user_id: str, right: DataSubjectRight, 
                                    request_data: Dict = None) -> Dict:
        """Handle GDPR data subject request."""
        if right == DataSubjectRight.ACCESS:
            return self._handle_access_request(user_id)
        elif right == DataSubjectRight.RECTIFICATION:
            return self._handle_rectification_request(user_id, request_data)
        elif right == DataSubjectRight.ERASURE:
            return self._handle_erasure_request(user_id)
        elif right == DataSubjectRight.PORTABILITY:
            return self._handle_portability_request(user_id)
        else:
            return {"status": "not_implemented", "right": right.value}
    
    def _handle_access_request(self, user_id: str) -> Dict:
        """Handle GDPR access request."""
        user_data = self.user_data.get(user_id, {})
        
        return {
            "user_id": user_id,
            "data": user_data,
            "consent_records": self.user_consent.get(user_id, []),
            "processing_logs": [
                log for log in self.data_processing_logs 
                if log.get("user_id") == user_id
            ]
        }
    
    def _handle_rectification_request(self, user_id: str, corrections: Dict) -> Dict:
        """Handle GDPR rectification request."""
        if user_id not in self.user_data:
            return {"status": "error", "message": "User not found"}
        
        # Update user data
        self.user_data[user_id].update(corrections)
        
        # Log rectification
        self._log_data_processing(
            user_id,
            "rectification",
            {"corrections": corrections}
        )
        
        return {"status": "success", "message": "Data rectified"}
    
    def _handle_erasure_request(self, user_id: str) -> Dict:
        """Handle GDPR erasure (right to be forgotten) request."""
        # Delete user data
        if user_id in self.user_data:
            del self.user_data[user_id]
        
        if user_id in self.user_consent:
            del self.user_consent[user_id]
        
        # Log erasure
        self._log_data_processing(
            user_id,
            "erasure",
            {"timestamp": datetime.utcnow().isoformat()}
        )
        
        return {"status": "success", "message": "Data erased"}
    
    def _handle_portability_request(self, user_id: str) -> Dict:
        """Handle GDPR data portability request."""
        user_data = self.user_data.get(user_id, {})
        consent_records = self.user_consent.get(user_id, [])
        
        # Format data in portable format (JSON)
        portable_data = {
            "user_id": user_id,
            "export_date": datetime.utcnow().isoformat(),
            "personal_data": user_data,
            "consent_history": consent_records
        }
        
        return {"status": "success", "data": portable_data}
    
    def record_user_consent(self, user_id: str, purpose: str, granted: bool):
        """Record user consent for data processing."""
        if user_id not in self.user_consent:
            self.user_consent[user_id] = []
        
        self.user_consent[user_id].append({
            "purpose": purpose,
            "granted": granted,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def _log_data_processing(self, user_id: str, operation: str, details: Dict):
        """Log data processing operations."""
        self.data_processing_logs.append({
            "user_id": user_id,
            "operation": operation,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details
        })