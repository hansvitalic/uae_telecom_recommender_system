"""
Cybersecurity sector module for UAE Telecom Recommender System.
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Any
from .base_sector import BaseSector, RiskAssessment, ProjectData


class CybersecuritySector(BaseSector):
    """Cybersecurity sector risk assessment module."""
    
    def _initialize_parameters(self) -> None:
        """Initialize cybersecurity specific parameters."""
        # Threat categories and their base risk levels
        self.threat_categories = {
            'external_attacks': 0.7,
            'insider_threats': 0.4,
            'malware': 0.6,
            'phishing': 0.5,
            'ddos': 0.6,
            'ransomware': 0.8,
            'data_breaches': 0.9,
            'supply_chain_attacks': 0.5
        }
        
        # Security controls and their risk reduction factors
        self.security_controls = {
            'firewall': 0.3,
            'intrusion_detection': 0.4,
            'encryption': 0.5,
            'multi_factor_authentication': 0.4,
            'security_training': 0.3,
            'vulnerability_management': 0.5,
            'backup_systems': 0.4,
            'incident_response': 0.4,
            'access_controls': 0.4,
            'security_monitoring': 0.5
        }
        
        # UAE-specific compliance requirements
        self.uae_compliance_requirements = {
            'uae_cyber_security_law': 0.8,
            'data_protection_law': 0.7,
            'tra_regulations': 0.6,
            'banking_regulations': 0.7,
            'critical_infrastructure': 0.9
        }
        
        # Technology risk factors
        self.technology_risks = {
            'cloud_services': 0.4,
            'iot_devices': 0.6,
            'mobile_apps': 0.5,
            'apis': 0.5,
            'third_party_integrations': 0.6,
            'legacy_systems': 0.8
        }
    
    def assess_risk(self, project_data: ProjectData) -> RiskAssessment:
        """Assess cybersecurity risk for a project."""
        base_risk = self.calculate_base_risk_score(project_data)
        
        # Calculate cybersecurity-specific risk factors
        threat_risk = self._assess_threat_landscape(project_data)
        compliance_risk = self._assess_compliance_risk(project_data)
        technology_risk = self._assess_technology_security_risk(project_data)
        data_risk = self._assess_data_protection_risk(project_data)
        
        # Calculate security controls effectiveness
        controls_effectiveness = self._assess_security_controls(project_data)
        
        # Combine all risk factors
        total_risk = (
            base_risk * 0.2 +
            threat_risk * 0.25 +
            compliance_risk * 0.2 +
            technology_risk * 0.2 +
            data_risk * 0.15
        )
        
        # Adjust for security controls (reduce risk)
        adjusted_risk = total_risk * (1.0 - controls_effectiveness * 0.5)
        
        # Apply sector weight
        weighted_risk = min(adjusted_risk * self.weight * 10, 1.0)
        
        # Identify active risk factors
        active_risk_factors = self._identify_active_risk_factors(
            threat_risk, compliance_risk, technology_risk, data_risk
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
    
    def _assess_threat_landscape(self, project_data: ProjectData) -> float:
        """Assess current threat landscape risks."""
        threat_score = 0.5  # Base threat level for UAE telecom
        
        # Check for high-risk technologies
        high_risk_keywords = ['internet-facing', 'public', 'external', 'customer-facing']
        for keyword in high_risk_keywords:
            if keyword in project_data.description.lower():
                threat_score += 0.2
        
        # Budget size correlates with attack attractiveness
        if project_data.budget > 10000000:  # 10M AED
            threat_score += 0.2
        elif project_data.budget > 5000000:  # 5M AED
            threat_score += 0.1
        
        # Long projects have more exposure time
        if project_data.timeline_days > 365:
            threat_score += 0.1
        
        return min(threat_score, 1.0)
    
    def _assess_compliance_risk(self, project_data: ProjectData) -> float:
        """Assess UAE regulatory compliance risks."""
        compliance_risk = 0.6  # Base compliance risk for telecom
        
        # Check for compliance-related keywords
        compliance_keywords = ['personal data', 'customer information', 'financial', 'critical infrastructure']
        for keyword in compliance_keywords:
            if keyword in project_data.description.lower():
                compliance_risk += 0.2
        
        # Cross-border data handling increases compliance complexity
        international_keywords = ['international', 'cross-border', 'global', 'offshore']
        for keyword in international_keywords:
            if keyword in project_data.description.lower():
                compliance_risk += 0.3
        
        return min(compliance_risk, 1.0)
    
    def _assess_technology_security_risk(self, project_data: ProjectData) -> float:
        """Assess technology-specific security risks."""
        tech_risk = 0.0
        
        for tech in project_data.technologies:
            tech_lower = tech.lower()
            
            # Check against known risky technologies
            for risk_tech, risk_level in self.technology_risks.items():
                if risk_tech.replace('_', ' ') in tech_lower or risk_tech in tech_lower:
                    tech_risk += risk_level
        
        # New/emerging technologies have unknown risks
        emerging_keywords = ['ai', 'machine learning', 'blockchain', '5g', 'edge computing']
        for keyword in emerging_keywords:
            if any(keyword in tech.lower() for tech in project_data.technologies):
                tech_risk += 0.4
        
        return min(tech_risk / max(len(project_data.technologies), 1), 1.0)
    
    def _assess_data_protection_risk(self, project_data: ProjectData) -> float:
        """Assess data protection and privacy risks."""
        data_risk = 0.3  # Base data protection risk
        
        # Check for data-related keywords
        data_keywords = ['database', 'customer data', 'personal information', 'analytics', 'reporting']
        for keyword in data_keywords:
            if keyword in project_data.description.lower():
                data_risk += 0.2
        
        # Multiple stakeholders increase data exposure risk
        if len(project_data.stakeholders) > 10:
            data_risk += 0.2
        
        # Dependencies increase data flow complexity
        if len(project_data.dependencies) > 5:
            data_risk += 0.1
        
        return min(data_risk, 1.0)
    
    def _assess_security_controls(self, project_data: ProjectData) -> float:
        """Assess effectiveness of planned security controls."""
        controls_score = 0.0
        controls_found = 0
        
        # Look for security controls mentioned in project
        description_lower = project_data.description.lower()
        for tech in project_data.technologies:
            tech_lower = tech.lower()
            
            for control, effectiveness in self.security_controls.items():
                control_terms = control.replace('_', ' ')
                if (control_terms in description_lower or 
                    control_terms in tech_lower or 
                    control in tech_lower):
                    controls_score += effectiveness
                    controls_found += 1
        
        # Return average effectiveness of found controls
        if controls_found > 0:
            return min(controls_score / controls_found, 1.0)
        else:
            return 0.1  # Minimal security if no controls mentioned
    
    def _identify_active_risk_factors(self, threat_risk: float, compliance_risk: float,
                                    tech_risk: float, data_risk: float) -> List[str]:
        """Identify which cybersecurity risk factors are most relevant."""
        active_factors = []
        
        if threat_risk > 0.6:
            active_factors.extend(["Cyber attacks", "System vulnerabilities"])
        if compliance_risk > 0.6:
            active_factors.append("Compliance violations")
        if tech_risk > 0.5:
            active_factors.append("System vulnerabilities")
        if data_risk > 0.5:
            active_factors.append("Data breaches")
        
        # Always include insider threats as baseline risk
        active_factors.append("Insider threats")
        
        return list(set(active_factors))  # Remove duplicates
    
    def _get_mitigation_strategies(self, risk_factors: List[str]) -> List[str]:
        """Get specific cybersecurity mitigation strategies."""
        strategies = self.get_common_mitigation_strategies()
        
        # Add cybersecurity specific strategies
        cyber_strategies = [
            "Implement multi-layered security controls (Defense in Depth)",
            "Conduct regular security assessments and penetration testing",
            "Establish Security Operations Center (SOC) monitoring",
            "Deploy advanced threat detection and response systems",
            "Implement zero-trust network architecture",
            "Conduct regular security awareness training for all staff",
            "Establish incident response and business continuity plans",
            "Implement data encryption at rest and in transit",
            "Deploy endpoint detection and response (EDR) solutions",
            "Maintain up-to-date vulnerability management program",
            "Implement privileged access management controls",
            "Establish secure software development lifecycle (SDLC)",
            "Deploy network segmentation and micro-segmentation",
            "Implement continuous compliance monitoring",
            "Establish threat intelligence and information sharing"
        ]
        
        strategies.extend(cyber_strategies)
        return strategies[:12]  # Limit to top 12 recommendations
    
    def get_recommendations(self, risk_assessment: RiskAssessment) -> List[str]:
        """Get actionable cybersecurity recommendations."""
        recommendations = []
        
        if risk_assessment.risk_level > 0.8:
            recommendations.extend([
                "URGENT: Conduct immediate security risk assessment",
                "Implement emergency incident response procedures",
                "Deploy advanced security monitoring and alerting",
                "Engage external cybersecurity expertise",
                "Review and strengthen access controls immediately"
            ])
        elif risk_assessment.risk_level > 0.6:
            recommendations.extend([
                "Conduct comprehensive security audit",
                "Implement additional security controls",
                "Enhance security monitoring capabilities",
                "Provide targeted security training",
                "Review compliance with UAE regulations"
            ])
        elif risk_assessment.risk_level > 0.4:
            recommendations.extend([
                "Maintain current security posture",
                "Schedule regular security reviews",
                "Update security policies and procedures",
                "Continue security awareness programs"
            ])
        else:
            recommendations.extend([
                "Continue baseline security practices",
                "Monitor for emerging threats",
                "Maintain security documentation"
            ])
        
        return recommendations[:8]  # Focus on top priorities