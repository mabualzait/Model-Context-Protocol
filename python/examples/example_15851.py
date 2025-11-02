# 📖 Chapter: Chapter 12: Compliance and Governance
# 📖 Section: 12.3 Compliance Frameworks

class ISO27001ComplianceManager:
    """Manage ISO 27001 compliance."""
    
    def __init__(self):
        self.security_controls: Dict[str, Dict] = {}
        self.risk_assessments: List[Dict] = []
        self.incident_logs: List[Dict] = []
    
    def assess_risk(self, asset: str, threats: List[str], 
                   vulnerabilities: List[str]) -> Dict:
        """Perform risk assessment."""
        risk_score = self._calculate_risk_score(threats, vulnerabilities)
        
        assessment = {
            "asset": asset,
            "threats": threats,
            "vulnerabilities": vulnerabilities,
            "risk_score": risk_score,
            "risk_level": self._classify_risk(risk_score),
            "recommendations": self._generate_risk_recommendations(risk_score),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.risk_assessments.append(assessment)
        
        return assessment
    
    def _calculate_risk_score(self, threats: List[str], 
                             vulnerabilities: List[str]) -> float:
        """Calculate risk score."""
        # Simplified risk calculation
        threat_score = len(threats) * 10
        vulnerability_score = len(vulnerabilities) * 15
        
        return (threat_score + vulnerability_score) / 2
    
    def _classify_risk(self, risk_score: float) -> str:
        """Classify risk level."""
        if risk_score >= 75:
            return "critical"
        elif risk_score >= 50:
            return "high"
        elif risk_score >= 25:
            return "medium"
        else:
            return "low"
    
    def _generate_risk_recommendations(self, risk_score: float) -> List[str]:
        """Generate risk mitigation recommendations."""
        recommendations = []
        
        if risk_score >= 75:
            recommendations.append("Immediate action required")
            recommendations.append("Implement additional security controls")
            recommendations.append("Conduct detailed security audit")
        elif risk_score >= 50:
            recommendations.append("Review security controls")
            recommendations.append("Implement additional safeguards")
        
        return recommendations