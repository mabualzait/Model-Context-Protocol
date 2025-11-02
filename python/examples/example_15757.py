# 📖 Chapter: Chapter 12: Compliance and Governance
# 📖 Section: 12.2 Regulatory Considerations for AI Integrations

class AIBiasMonitor:
    """Monitor AI systems for bias and fairness."""
    
    def __init__(self):
        self.bias_metrics: Dict[str, Dict] = {}
        self.fairness_reports: List[Dict] = []
    
    def analyze_fairness(self, model_name: str, decisions: List[Dict]) -> Dict:
        """Analyze fairness of AI decisions."""
        # Group decisions by protected attributes
        protected_groups = self._group_by_protected_attributes(decisions)
        
        # Calculate fairness metrics
        fairness_metrics = {}
        for group, group_decisions in protected_groups.items():
            fairness_metrics[group] = self._calculate_fairness_metrics(group_decisions)
        
        # Check for bias
        bias_detected = self._detect_bias(fairness_metrics)
        
        report = {
            "model_name": model_name,
            "timestamp": datetime.utcnow().isoformat(),
            "fairness_metrics": fairness_metrics,
            "bias_detected": bias_detected,
            "recommendations": self._generate_recommendations(bias_detected)
        }
        
        self.fairness_reports.append(report)
        
        return report
    
    def _group_by_protected_attributes(self, decisions: List[Dict]) -> Dict[str, List[Dict]]:
        """Group decisions by protected attributes."""
        protected_attributes = ["gender", "race", "age", "disability"]
        groups = {}
        
        for decision in decisions:
            attributes = decision.get("protected_attributes", {})
            group_key = "_".join([
                f"{attr}={attributes.get(attr, 'unknown')}"
                for attr in protected_attributes
                if attr in attributes
            ])
            
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(decision)
        
        return groups
    
    def _calculate_fairness_metrics(self, decisions: List[Dict]) -> Dict:
        """Calculate fairness metrics for group."""
        if not decisions:
            return {}
        
        positive_outcomes = sum(1 for d in decisions if d.get("outcome") == "positive")
        total = len(decisions)
        
        return {
            "positive_rate": positive_outcomes / total if total > 0 else 0,
            "total_decisions": total,
            "positive_outcomes": positive_outcomes
        }
    
    def _detect_bias(self, fairness_metrics: Dict) -> bool:
        """Detect bias in fairness metrics."""
        if len(fairness_metrics) < 2:
            return False
        
        rates = [metrics["positive_rate"] for metrics in fairness_metrics.values()]
        max_rate = max(rates)
        min_rate = min(rates)
        
        # Bias detected if difference > 20%
        return (max_rate - min_rate) > 0.20
    
    def _generate_recommendations(self, bias_detected: bool) -> List[str]:
        """Generate recommendations based on bias analysis."""
        recommendations = []
        
        if bias_detected:
            recommendations.append("Review training data for representativeness")
            recommendations.append("Consider using fairness-aware algorithms")
            recommendations.append("Implement bias mitigation techniques")
        
        return recommendations