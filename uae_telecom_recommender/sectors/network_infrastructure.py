"""
Network Infrastructure sector module for UAE Telecom Recommender System.
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Any
from .base_sector import BaseSector, RiskAssessment, ProjectData


class NetworkInfrastructureSector(BaseSector):
    """Network Infrastructure sector risk assessment module."""
    
    def _initialize_parameters(self) -> None:
        """Initialize network infrastructure specific parameters."""
        # Critical infrastructure components and their risk multipliers
        self.infrastructure_components = {
            'fiber_optic': 0.3,
            'cellular_towers': 0.4,
            'data_centers': 0.5,
            'switches_routers': 0.4,
            'transmission_equipment': 0.3,
            'power_systems': 0.6,
            'cooling_systems': 0.4,
            'security_systems': 0.3
        }
        
        # UAE-specific environmental risk factors
        self.environmental_risks = {
            'sandstorm': 0.4,
            'extreme_heat': 0.5,
            'humidity': 0.3,
            'dust': 0.4,
            'flooding': 0.2
        }
        
        # Technology obsolescence factors
        self.technology_age_risks = {
            'legacy': 0.8,
            'mature': 0.4,
            'current': 0.2,
            'emerging': 0.6
        }
    
    def assess_risk(self, project_data: ProjectData) -> RiskAssessment:
        """Assess network infrastructure risk for a project."""
        base_risk = self.calculate_base_risk_score(project_data)
        
        # Calculate infrastructure-specific risk factors
        infrastructure_risk = self._assess_infrastructure_risk(project_data)
        environmental_risk = self._assess_environmental_risk(project_data)
        technology_risk = self._assess_technology_risk(project_data)
        capacity_risk = self._assess_capacity_risk(project_data)
        
        # Combine all risk factors with weights
        total_risk = (
            base_risk * 0.3 +
            infrastructure_risk * 0.25 +
            environmental_risk * 0.2 +
            technology_risk * 0.15 +
            capacity_risk * 0.1
        )
        
        # Apply sector weight
        weighted_risk = min(total_risk * self.weight * 10, 1.0)  # Scale by weight
        
        # Determine primary risk factors
        active_risk_factors = self._identify_active_risk_factors(
            infrastructure_risk, environmental_risk, technology_risk, capacity_risk
        )
        
        # Get mitigation strategies
        mitigation_strategies = self._get_mitigation_strategies(active_risk_factors)
        
        # Calculate confidence
        confidence = self.calculate_confidence_score(project_data)
        
        return RiskAssessment(
            sector_id=self.sector_id,
            risk_level=weighted_risk,
            risk_factors=active_risk_factors,
            mitigation_strategies=mitigation_strategies,
            confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
    
    def _assess_infrastructure_risk(self, project_data: ProjectData) -> float:
        """Assess infrastructure-related risks."""
        risk_score = 0.0
        
        # Analyze mentioned infrastructure components
        for tech in project_data.technologies:
            tech_lower = tech.lower()
            for component, risk_multiplier in self.infrastructure_components.items():
                if component.replace('_', ' ') in tech_lower or component in tech_lower:
                    risk_score += risk_multiplier
        
        # Consider project complexity for infrastructure
        complexity_multiplier = 1.0 + (project_data.complexity_score * 0.5)
        risk_score *= complexity_multiplier
        
        return min(risk_score / len(self.infrastructure_components), 1.0)
    
    def _assess_environmental_risk(self, project_data: ProjectData) -> float:
        """Assess UAE environmental risk factors."""
        # Base environmental risk for UAE telecom infrastructure
        base_environmental_risk = 0.4
        
        # Adjust based on project timeline (longer projects = more exposure)
        timeline_factor = min(project_data.timeline_days / 365, 2.0)
        
        # Outdoor infrastructure has higher environmental risk
        outdoor_keywords = ['tower', 'outdoor', 'external', 'field', 'installation']
        outdoor_risk = 0.0
        for keyword in outdoor_keywords:
            if keyword in project_data.description.lower():
                outdoor_risk += 0.2
        
        environmental_risk = base_environmental_risk + (timeline_factor * 0.1) + outdoor_risk
        return min(environmental_risk, 1.0)
    
    def _assess_technology_risk(self, project_data: ProjectData) -> float:
        """Assess technology-related risks."""
        technology_risk = 0.0
        
        # Assess each technology mentioned
        for tech in project_data.technologies:
            tech_lower = tech.lower()
            
            # Check for technology age indicators
            if any(word in tech_lower for word in ['legacy', 'old', 'deprecated']):
                technology_risk += self.technology_age_risks['legacy']
            elif any(word in tech_lower for word in ['new', 'emerging', 'beta', 'cutting-edge']):
                technology_risk += self.technology_age_risks['emerging']
            elif any(word in tech_lower for word in ['5g', 'ai', 'iot', 'edge']):
                technology_risk += self.technology_age_risks['emerging']
            else:
                technology_risk += self.technology_age_risks['current']
        
        return min(technology_risk / max(len(project_data.technologies), 1), 1.0)
    
    def _assess_capacity_risk(self, project_data: ProjectData) -> float:
        """Assess network capacity and scalability risks."""
        capacity_risk = 0.3  # Base capacity risk
        
        # High budget projects may strain capacity
        if project_data.budget > 5000000:  # 5M AED
            capacity_risk += 0.2
        
        # Multiple dependencies increase capacity risk
        if len(project_data.dependencies) > 5:
            capacity_risk += 0.3
        
        # Check for capacity-related keywords
        capacity_keywords = ['scaling', 'expansion', 'upgrade', 'capacity', 'bandwidth']
        for keyword in capacity_keywords:
            if keyword in project_data.description.lower():
                capacity_risk += 0.1
        
        return min(capacity_risk, 1.0)
    
    def _identify_active_risk_factors(self, infra_risk: float, env_risk: float, 
                                    tech_risk: float, capacity_risk: float) -> List[str]:
        """Identify which risk factors are most relevant."""
        active_factors = []
        
        if infra_risk > 0.5:
            active_factors.append("Equipment failure")
        if env_risk > 0.4:
            active_factors.append("Infrastructure damage")
        if tech_risk > 0.5:
            active_factors.append("Technology obsolescence")
        if capacity_risk > 0.4:
            active_factors.append("Capacity limitations")
        
        # Always include network congestion as a baseline risk
        active_factors.append("Network congestion")
        
        return active_factors
    
    def _get_mitigation_strategies(self, risk_factors: List[str]) -> List[str]:
        """Get specific mitigation strategies for identified risks."""
        strategies = self.get_common_mitigation_strategies()
        
        # Add network infrastructure specific strategies
        network_strategies = [
            "Implement redundant network paths and equipment",
            "Regular maintenance and equipment health monitoring",
            "Environmental protection systems for outdoor equipment",
            "Capacity planning and traffic management",
            "Technology refresh cycles and upgrade planning",
            "Network performance monitoring and alerting",
            "Emergency response procedures for infrastructure failures",
            "Backup power systems and uninterruptible power supplies",
            "Climate control systems for equipment rooms",
            "Network security hardening and access controls"
        ]
        
        strategies.extend(network_strategies)
        return strategies[:10]  # Limit to top 10 recommendations
    
    def get_recommendations(self, risk_assessment: RiskAssessment) -> List[str]:
        """Get actionable recommendations based on risk assessment."""
        recommendations = []
        
        if risk_assessment.risk_level > 0.7:
            recommendations.extend([
                "Conduct immediate infrastructure vulnerability assessment",
                "Implement comprehensive disaster recovery procedures",
                "Establish 24/7 network operations center monitoring"
            ])
        elif risk_assessment.risk_level > 0.5:
            recommendations.extend([
                "Schedule preventive maintenance for critical equipment",
                "Review and update capacity planning models",
                "Implement enhanced environmental monitoring"
            ])
        else:
            recommendations.extend([
                "Continue regular monitoring and maintenance schedules",
                "Plan for future technology upgrades",
                "Maintain current redundancy levels"
            ])
        
        return recommendations