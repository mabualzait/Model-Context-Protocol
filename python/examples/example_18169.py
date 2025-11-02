# 📖 Chapter: Chapter 14: MCP and Enterprise Integration
# 📖 Section: 14.5 Organizational Adoption Strategies

from enum import Enum
from typing import Dict, List

class AdoptionPhase(Enum):
    ASSESSMENT = "assessment"
    PILOT = "pilot"
    SCALING = "scaling"
    PRODUCTION = "production"

class MCPAdoptionManager:
    """Manage organizational adoption of MCP."""
    
    def __init__(self):
        self.adoption_phases = [
            AdoptionPhase.ASSESSMENT,
            AdoptionPhase.PILOT,
            AdoptionPhase.SCALING,
            AdoptionPhase.PRODUCTION
        ]
        self.current_phase = AdoptionPhase.ASSESSMENT
        self.readiness_scores: Dict[str, float] = {}
        self.milestones: List[Dict] = []
    
    def assess_readiness(self) -> Dict:
        """Assess organizational readiness for MCP."""
        technical_score = self._assess_technical_readiness()
        organizational_score = self._assess_organizational_readiness()
        process_score = self._assess_process_readiness()
        
        overall_score = (technical_score + organizational_score + process_score) / 3
        
        return {
            "overall_score": overall_score,
            "technical_readiness": {
                "score": technical_score,
                "factors": self._get_technical_factors()
            },
            "organizational_readiness": {
                "score": organizational_score,
                "factors": self._get_organizational_factors()
            },
            "process_readiness": {
                "score": process_score,
                "factors": self._get_process_factors()
            },
            "recommendations": self._generate_recommendations(overall_score)
        }
    
    def _assess_technical_readiness(self) -> float:
        """Assess technical readiness (0-100)."""
        factors = {
            "infrastructure": 20,  # Cloud infrastructure, containers
            "expertise": 25,  # Development skills, MCP knowledge
            "tooling": 15,  # CI/CD, monitoring, testing tools
            "security": 20,  # Security practices, compliance
            "documentation": 10,  # Technical documentation
            "standards": 10  # Coding standards, best practices
        }
        
        scores = {}
        total_score = 0
        
        # Simplified scoring (in practice, detailed assessment)
        for factor, weight in factors.items():
            score = 70  # Default moderate score
            scores[factor] = score
            total_score += score * weight / 100
        
        return min(total_score, 100)
    
    def _assess_organizational_readiness(self) -> float:
        """Assess organizational readiness (0-100)."""
        factors = {
            "leadership_support": 30,
            "team_alignment": 25,
            "change_capacity": 20,
            "communication": 15,
            "training": 10
        }
        
        total_score = 0
        for factor, weight in factors.items():
            score = 65  # Default score
            total_score += score * weight / 100
        
        return min(total_score, 100)
    
    def _assess_process_readiness(self) -> float:
        """Assess process readiness (0-100)."""
        factors = {
            "development_process": 25,
            "deployment_process": 25,
            "monitoring_process": 20,
            "incident_management": 15,
            "change_management": 15
        }
        
        total_score = 0
        for factor, weight in factors.items():
            score = 70  # Default score
            total_score += score * weight / 100
        
        return min(total_score, 100)
    
    def _get_technical_factors(self) -> List[str]:
        """Get technical assessment factors."""
        return [
            "Infrastructure capability",
            "Development expertise",
            "Tooling and automation",
            "Security maturity",
            "Documentation quality",
            "Standards compliance"
        ]
    
    def _get_organizational_factors(self) -> List[str]:
        """Get organizational assessment factors."""
        return [
            "Leadership support and sponsorship",
            "Team alignment and buy-in",
            "Change management capacity",
            "Communication effectiveness",
            "Training and skills development"
        ]
    
    def _get_process_factors(self) -> List[str]:
        """Get process assessment factors."""
        return [
            "Development workflow maturity",
            "Deployment automation",
            "Monitoring and observability",
            "Incident response procedures",
            "Change management process"
        ]
    
    def _generate_recommendations(self, score: float) -> List[str]:
        """Generate recommendations based on readiness score."""
        recommendations = []
        
        if score < 50:
            recommendations.append("Focus on building foundational capabilities first")
            recommendations.append("Start with technical training and infrastructure setup")
            recommendations.append("Engage leadership to secure organizational support")
        elif score < 70:
            recommendations.append("Begin with a small pilot project")
            recommendations.append("Address identified gaps in readiness assessment")
            recommendations.append("Establish monitoring and success metrics")
        else:
            recommendations.append("Ready for pilot deployment")
            recommendations.append("Scale gradually with measured success")
            recommendations.append("Document lessons learned and best practices")
        
        return recommendations
    
    def create_pilot_plan(self, scope: Dict) -> Dict:
        """Create pilot project plan."""
        return {
            "pilot_name": scope.get("name", "MCP Pilot"),
            "scope": scope,
            "timeline": scope.get("timeline", "12 weeks"),
            "success_criteria": scope.get("success_criteria", []),
            "risks": scope.get("risks", []),
            "mitigation": scope.get("mitigation", []),
            "resources": scope.get("resources", []),
            "milestones": self._define_milestones()
        }
    
    def _define_milestones(self) -> List[Dict]:
        """Define pilot project milestones."""
        return [
            {
                "phase": "week_1_2",
                "milestone": "Infrastructure setup complete",
                "deliverables": ["MCP server instances", "Monitoring setup"]
            },
            {
                "phase": "week_3_4",
                "milestone": "First MCP server implemented",
                "deliverables": ["Working MCP server", "Integration tests"]
            },
            {
                "phase": "week_5_8",
                "milestone": "Pilot integration with AI assistant",
                "deliverables": ["AI integration", "User acceptance testing"]
            },
            {
                "phase": "week_9_12",
                "milestone": "Pilot evaluation complete",
                "deliverables": ["Evaluation report", "Scaling recommendations"]
            }
        ]
    
    def transition_to_next_phase(self):
        """Transition to next adoption phase."""
        current_index = self.adoption_phases.index(self.current_phase)
        if current_index < len(self.adoption_phases) - 1:
            self.current_phase = self.adoption_phases[current_index + 1]
            return True
        return False
    
    def get_current_phase(self) -> AdoptionPhase:
        """Get current adoption phase."""
        return self.current_phase

class ChangeManagementPlan:
    """Manage change for MCP adoption."""
    
    def __init__(self):
        self.stakeholders: List[Dict] = []
        self.communication_plan: List[Dict] = []
        self.training_plan: List[Dict] = []
    
    def identify_stakeholders(self) -> List[Dict]:
        """Identify key stakeholders."""
        return [
            {"role": "executive_sponsor", "influence": "high", "interest": "high"},
            {"role": "technical_lead", "influence": "high", "interest": "high"},
            {"role": "developers", "influence": "medium", "interest": "high"},
            {"role": "operations", "influence": "medium", "interest": "medium"},
            {"role": "end_users", "influence": "low", "interest": "high"}
        ]
    
    def create_communication_plan(self) -> List[Dict]:
        """Create communication plan."""
        return [
            {
                "audience": "executives",
                "message": "Business value and ROI of MCP adoption",
                "frequency": "monthly",
                "channel": "executive_report"
            },
            {
                "audience": "technical_teams",
                "message": "Technical benefits and implementation details",
                "frequency": "weekly",
                "channel": "tech_meeting"
            },
            {
                "audience": "all_staff",
                "message": "Progress updates and success stories",
                "frequency": "biweekly",
                "channel": "newsletter"
            }
        ]
    
    def create_training_plan(self) -> List[Dict]:
        """Create training plan."""
        return [
            {
                "audience": "developers",
                "topics": ["MCP fundamentals", "Server development", "Client integration"],
                "format": "hands_on_workshop",
                "duration": "2_days"
            },
            {
                "audience": "architects",
                "topics": ["Architecture patterns", "Enterprise integration", "Security"],
                "format": "architecture_session",
                "duration": "1_day"
            },
            {
                "audience": "operations",
                "topics": ["Deployment", "Monitoring", "Troubleshooting"],
                "format": "operational_training",
                "duration": "1_day"
            }
        ]