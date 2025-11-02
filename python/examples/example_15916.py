# 📖 Chapter: Chapter 12: Compliance and Governance
# 📖 Section: 12.3 Compliance Frameworks

class SOC2ComplianceManager:
    """Manage SOC 2 compliance."""
    
    def __init__(self):
        self.trust_service_criteria = {
            "security": [],
            "availability": [],
            "processing_integrity": [],
            "confidentiality": [],
            "privacy": []
        }
        self.control_tests: List[Dict] = []
    
    def test_control(self, criterion: str, control_id: str, test_result: bool):
        """Test control effectiveness."""
        self.control_tests.append({
            "criterion": criterion,
            "control_id": control_id,
            "test_result": test_result,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        if criterion in self.trust_service_criteria:
            self.trust_service_criteria[criterion].append({
                "control_id": control_id,
                "test_result": test_result,
                "timestamp": datetime.utcnow().isoformat()
            })
    
    def generate_soc2_report(self) -> Dict:
        """Generate SOC 2 compliance report."""
        return {
            "trust_service_criteria": {
                criterion: {
                    "total_controls": len(controls),
                    "passed_controls": sum(1 for c in controls if c["test_result"]),
                    "failed_controls": sum(1 for c in controls if not c["test_result"]),
                    "compliance_rate": sum(1 for c in controls if c["test_result"]) / len(controls) if controls else 0
                }
                for criterion, controls in self.trust_service_criteria.items()
            },
            "overall_compliance": self._calculate_overall_compliance()
        }
    
    def _calculate_overall_compliance(self) -> float:
        """Calculate overall compliance rate."""
        total_tests = len(self.control_tests)
        passed_tests = sum(1 for test in self.control_tests if test["test_result"])
        
        return passed_tests / total_tests if total_tests > 0 else 0