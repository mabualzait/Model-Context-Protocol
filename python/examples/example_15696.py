# 📖 Chapter: Chapter 12: Compliance and Governance
# 📖 Section: 12.2 Regulatory Considerations for AI Integrations

class AITransparencyManager:
    """Manage AI transparency and explainability requirements."""
    
    def __init__(self):
        self.ai_decision_logs: List[Dict] = []
        self.model_documentation: Dict[str, Dict] = {}
    
    def log_ai_decision(self, decision_id: str, model_name: str, 
                       input_data: Dict, output: Dict, reasoning: str = None):
        """Log AI decision for transparency."""
        self.ai_decision_logs.append({
            "decision_id": decision_id,
            "model_name": model_name,
            "input_data": self._sanitize_input(input_data),
            "output": output,
            "reasoning": reasoning,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def explain_decision(self, decision_id: str) -> Dict:
        """Provide explanation for AI decision."""
        decision = next(
            (d for d in self.ai_decision_logs if d["decision_id"] == decision_id),
            None
        )
        
        if not decision:
            return {"status": "error", "message": "Decision not found"}
        
        model_info = self.model_documentation.get(decision["model_name"], {})
        
        return {
            "decision_id": decision_id,
            "model_name": decision["model_name"],
            "model_description": model_info.get("description", ""),
            "input_data": decision["input_data"],
            "output": decision["output"],
            "reasoning": decision.get("reasoning", ""),
            "model_metadata": model_info
        }
    
    def _sanitize_input(self, input_data: Dict) -> Dict:
        """Sanitize input data for logging."""
        # Remove sensitive information
        sensitive_keys = {"password", "api_key", "secret", "token"}
        sanitized = {}
        
        for key, value in input_data.items():
            if key.lower() in sensitive_keys:
                sanitized[key] = "***MASKED***"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_input(value)
            else:
                sanitized[key] = value
        
        return sanitized