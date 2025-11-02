# 📖 Chapter: Chapter 15: The Future of MCP
# 📖 Section: 15.1 Emerging Trends and Research Directions

class EcosystemGrowthTracker:
    """Track MCP ecosystem growth."""
    
    def __init__(self):
        self.metrics = {
            "server_implementations": 0,
            "client_libraries": 0,
            "community_servers": 0,
            "documentation_pages": 0,
            "github_stars": 0,
            "contributors": 0
        }
        self.growth_history: List[Dict] = []
    
    def record_ecosystem_metrics(self):
        """Record current ecosystem metrics."""
        snapshot = {
            "timestamp": time.time(),
            "metrics": dict(self.metrics)
        }
        self.growth_history.append(snapshot)
    
    def calculate_growth_rate(self, period_days: int = 30) -> Dict:
        """Calculate growth rate over period."""
        cutoff = time.time() - (period_days * 24 * 3600)
        recent_snapshots = [
            s for s in self.growth_history
            if s["timestamp"] > cutoff
        ]
        
        if len(recent_snapshots) < 2:
            return {"error": "Insufficient data"}
        
        first = recent_snapshots[0]["metrics"]
        last = recent_snapshots[-1]["metrics"]
        
        growth_rates = {}
        for key in first.keys():
            if first[key] > 0:
                growth_rate = ((last[key] - first[key]) / first[key]) * 100
                growth_rates[key] = growth_rate
        
        return growth_rates