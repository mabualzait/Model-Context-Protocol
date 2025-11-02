# 📖 Chapter: Chapter 12: Compliance and Governance
# 📖 Section: 12.4 Risk Management

from typing import List, Dict
from enum import Enum

class RiskLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class RiskManager:
    """Manage risks in MCP systems."""
    
    def __init__(self):
        self.risks: Dict[str, Dict] = {}
        self.risk_mitigations: Dict[str, List[Dict]] = {}
    
    def identify_risk(self, risk_id: str, description: str, 
                     likelihood: float, impact: float, category: str) -> Dict:
        """Identify and register risk."""
        risk_score = likelihood * impact
        
        risk = {
            "risk_id": risk_id,
            "description": description,
            "likelihood": likelihood,
            "impact": impact,
            "risk_score": risk_score,
            "risk_level": self._classify_risk_level(risk_score),
            "category": category,
            "identified_at": datetime.utcnow().isoformat(),
            "status": "open"
        }
        
        self.risks[risk_id] = risk
        
        return risk
    
    def add_mitigation(self, risk_id: str, mitigation: Dict):
        """Add mitigation strategy for risk."""
        if risk_id not in self.risks:
            raise ValueError(f"Risk {risk_id} not found")
        
        if risk_id not in self.risk_mitigations:
            self.risk_mitigations[risk_id] = []
        
        mitigation["added_at"] = datetime.utcnow().isoformat()
        self.risk_mitigations[risk_id].append(mitigation)
    
    def evaluate_mitigation(self, risk_id: str) -> Dict:
        """Evaluate effectiveness of mitigations."""
        if risk_id not in self.risks:
            return {"status": "error", "message": "Risk not found"}
        
        risk = self.risks[risk_id]
        mitigations = self.risk_mitigations.get(risk_id, [])
        
        # Calculate residual risk
        mitigation_effectiveness = sum(
            m.get("effectiveness", 0) for m in mitigations
        )
        residual_risk_score = risk["risk_score"] * (1 - min(mitigation_effectiveness, 1.0))
        
        return {
            "risk_id": risk_id,
            "original_risk_score": risk["risk_score"],
            "residual_risk_score": residual_risk_score,
            "mitigation_effectiveness": mitigation_effectiveness,
            "residual_risk_level": self._classify_risk_level(residual_risk_score),
            "mitigations": mitigations
        }
    
    def _classify_risk_level(self, risk_score: float) -> str:
        """Classify risk level."""
        if risk_score >= 0.75:
            return RiskLevel.CRITICAL.value
        elif risk_score >= 0.50:
            return RiskLevel.HIGH.value
        elif risk_score >= 0.25:
            return RiskLevel.MEDIUM.value
        else:
            return RiskLevel.LOW.value