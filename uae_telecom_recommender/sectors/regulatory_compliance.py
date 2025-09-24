"""
Regulatory Compliance sector module for UAE Telecom Recommender System.
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Any
from .base_sector import BaseSector, RiskAssessment, ProjectData


class RegulatoryComplianceSector(BaseSector):
    """Regulatory Compliance sector risk assessment module."""
    
    def _initialize_parameters(self) -> None:
        """Initialize regulatory compliance specific parameters."""
        # UAE telecom regulatory frameworks
        self.regulatory_frameworks = {
            'tra_telecom_regulations': {
                'risk_level': 0.8,
                'keywords': ['telecom', 'telecommunication', 'network', 'spectrum', 'licensing']
            },
            'uae_cyber_security_law': {
                'risk_level': 0.9,
                'keywords': ['cybersecurity', 'information security', 'data protection', 'cyber']
            },
            'uae_data_protection_law': {
                'risk_level': 0.8,
                'keywords': ['personal data', 'privacy', 'data processing', 'customer information']
            },
            'consumer_protection_law': {
                'risk_level': 0.6,
                'keywords': ['consumer', 'customer service', 'billing', 'complaints']
            },
            'federal_law_competition': {
                'risk_level': 0.5,
                'keywords': ['competition', 'market', 'pricing', 'anti-monopoly']
            },
            'anti_money_laundering': {
                'risk_level': 0.7,
                'keywords': ['aml', 'financial', 'payment', 'money laundering', 'sanctions']
            },
            'critical_infrastructure': {
                'risk_level': 0.9,
                'keywords': ['critical infrastructure', 'national security', 'essential services']
            }
        }
        
        # Compliance risk factors by project type
        self.project_compliance_risks = {
            'new_service_launch': 0.8,
            'infrastructure_expansion': 0.7,
            'customer_facing': 0.6,
            'data_processing': 0.8,
            'international_connectivity': 0.9,
            'financial_services': 0.9,
            'government_services': 0.8
        }
        
        # Penalty severity levels
        self.penalty_levels = {
            'administrative_fine': 0.4,
            'service_suspension': 0.8,
            'license_revocation': 1.0,
            'criminal_charges': 1.0,
            'reputational_damage': 0.6
        }
    
    def assess_risk(self, project_data: ProjectData) -> RiskAssessment:
        """Assess regulatory compliance risk for a project."""
        base_risk = self.calculate_base_risk_score(project_data)
        
        # Calculate compliance-specific risk factors
        regulatory_framework_risk = self._assess_regulatory_framework_risk(project_data)
        license_compliance_risk = self._assess_license_compliance_risk(project_data)
        data_protection_risk = self._assess_data_protection_risk(project_data)
        audit_risk = self._assess_audit_readiness_risk(project_data)
        policy_compliance_risk = self._assess_policy_compliance_risk(project_data)
        
        # Combine all risk factors with weights
        total_risk = (
            base_risk * 0.15 +
            regulatory_framework_risk * 0.25 +
            license_compliance_risk * 0.2 +
            data_protection_risk * 0.2 +
            audit_risk * 0.1 +
            policy_compliance_risk * 0.1
        )
        
        # Apply sector weight
        weighted_risk = min(total_risk * self.weight * 10, 1.0)
        
        # Identify active risk factors
        active_risk_factors = self._identify_active_risk_factors(
            regulatory_framework_risk, license_compliance_risk, 
            data_protection_risk, audit_risk
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
    
    def _assess_regulatory_framework_risk(self, project_data: ProjectData) -> float:
        """Assess risk related to UAE regulatory frameworks."""
        framework_risk = 0.0
        applicable_frameworks = 0
        
        description_lower = project_data.description.lower()
        
        # Check which regulatory frameworks apply
        for framework, details in self.regulatory_frameworks.items():
            framework_applies = False
            for keyword in details['keywords']:
                if keyword in description_lower:
                    framework_applies = True
                    break
            
            if framework_applies:
                framework_risk += details['risk_level']
                applicable_frameworks += 1
        
        # High-budget projects attract more regulatory attention
        if project_data.budget > 50000000:  # 50M AED
            framework_risk += 0.3
        elif project_data.budget > 20000000:  # 20M AED
            framework_risk += 0.2
        
        # Multiple stakeholders increase compliance complexity
        if len(project_data.stakeholders) > 15:
            framework_risk += 0.2
        
        return min(framework_risk / max(applicable_frameworks, 1), 1.0)
    
    def _assess_license_compliance_risk(self, project_data: ProjectData) -> float:
        """Assess risks related to telecom licensing requirements."""
        license_risk = 0.4  # Base license compliance risk
        
        # Check for license-relevant activities
        license_keywords = [
            'new service', 'service launch', 'spectrum', 'frequency',
            'infrastructure deployment', 'network expansion', 'interconnection'
        ]
        
        for keyword in license_keywords:
            if keyword in project_data.description.lower():
                license_risk += 0.3
        
        # International connectivity requires special licenses
        international_keywords = ['international', 'cross-border', 'submarine cable', 'satellite']
        for keyword in international_keywords:
            if keyword in project_data.description.lower():
                license_risk += 0.4
        
        # Long timeline projects may face changing regulations
        if project_data.timeline_days > 730:  # 2 years
            license_risk += 0.2
        
        return min(license_risk, 1.0)
    
    def _assess_data_protection_risk(self, project_data: ProjectData) -> float:
        """Assess data protection and privacy compliance risks."""
        data_risk = 0.3  # Base data protection risk
        
        # Check for data-related activities
        data_keywords = [
            'customer data', 'personal information', 'data collection',
            'data processing', 'analytics', 'artificial intelligence',
            'machine learning', 'profiling', 'behavioral analysis'
        ]
        
        for keyword in data_keywords:
            if keyword in project_data.description.lower():
                data_risk += 0.2
        
        # Customer-facing projects have higher data protection requirements
        customer_keywords = ['customer portal', 'mobile app', 'web service', 'self-service']
        for keyword in customer_keywords:
            if keyword in project_data.description.lower():
                data_risk += 0.3
        
        # Cross-border data transfers are heavily regulated
        if any('international' in dep.lower() or 'offshore' in dep.lower() 
               for dep in project_data.dependencies):
            data_risk += 0.4
        
        return min(data_risk, 1.0)
    
    def _assess_audit_readiness_risk(self, project_data: ProjectData) -> float:
        """Assess readiness for regulatory audits and inspections."""
        audit_risk = 0.5  # Base audit readiness risk
        
        # Complex projects are more likely to be audited
        if project_data.complexity_score > 0.7:
            audit_risk += 0.2
        
        # Multiple dependencies make audit preparation harder
        if len(project_data.dependencies) > 8:
            audit_risk += 0.2
        
        # New technologies may not have established compliance procedures
        emerging_tech_keywords = ['ai', '5g', 'iot', 'blockchain', 'edge computing']
        for tech in project_data.technologies:
            if any(keyword in tech.lower() for keyword in emerging_tech_keywords):
                audit_risk += 0.1
        
        return min(audit_risk, 1.0)
    
    def _assess_policy_compliance_risk(self, project_data: ProjectData) -> float:
        """Assess risk of non-compliance with internal and external policies."""
        policy_risk = 0.4  # Base policy compliance risk
        
        # Projects with many stakeholders have policy alignment challenges
        if len(project_data.stakeholders) > 10:
            policy_risk += 0.2
        
        # Historical risks indicate policy compliance issues
        if project_data.historical_risks:
            compliance_history = [risk for risk in project_data.historical_risks 
                                if 'compliance' in risk.lower() or 'policy' in risk.lower()]
            if compliance_history:
                policy_risk += 0.3
        
        return min(policy_risk, 1.0)
    
    def _identify_active_risk_factors(self, framework_risk: float, license_risk: float,
                                    data_risk: float, audit_risk: float) -> List[str]:
        """Identify which regulatory compliance risk factors are most relevant."""
        active_factors = []
        
        if framework_risk > 0.6:
            active_factors.append("Regulatory violations")
        if license_risk > 0.5:
            active_factors.append("License compliance")
        if data_risk > 0.5:
            active_factors.append("Data protection breaches")
        if audit_risk > 0.5:
            active_factors.append("Audit failures")
        
        # Always include policy compliance as baseline
        active_factors.append("Policy non-compliance")
        
        return active_factors
    
    def _get_mitigation_strategies(self, risk_factors: List[str]) -> List[str]:
        """Get specific regulatory compliance mitigation strategies."""
        strategies = self.get_common_mitigation_strategies()
        
        # Add regulatory compliance specific strategies
        compliance_strategies = [
            "Establish dedicated compliance officer and team",
            "Conduct regular regulatory impact assessments",
            "Implement compliance monitoring and reporting systems",
            "Maintain current regulatory knowledge and tracking",
            "Establish relationships with regulatory authorities",
            "Conduct pre-launch compliance reviews",
            "Implement data protection impact assessments (DPIA)",
            "Establish audit trail and documentation procedures",
            "Create compliance training programs for staff",
            "Implement automated compliance monitoring tools",
            "Establish legal review processes for new initiatives",
            "Maintain compliance risk register and mitigation plans",
            "Conduct regular internal compliance audits",
            "Establish incident response procedures for compliance breaches",
            "Implement change management for regulatory updates"
        ]
        
        strategies.extend(compliance_strategies)
        return strategies[:12]  # Limit to top 12 recommendations
    
    def get_recommendations(self, risk_assessment: RiskAssessment) -> List[str]:
        """Get actionable regulatory compliance recommendations."""
        recommendations = []
        
        if risk_assessment.risk_level > 0.8:
            recommendations.extend([
                "URGENT: Conduct immediate compliance risk assessment",
                "Engage legal counsel for regulatory review",
                "Implement emergency compliance monitoring",
                "Contact relevant regulatory authorities for guidance",
                "Suspend project activities until compliance confirmed"
            ])
        elif risk_assessment.risk_level > 0.6:
            recommendations.extend([
                "Conduct comprehensive regulatory compliance review",
                "Engage compliance consultants for specialized expertise",
                "Implement enhanced compliance monitoring",
                "Review and update compliance policies and procedures",
                "Provide compliance training for project team"
            ])
        elif risk_assessment.risk_level > 0.4:
            recommendations.extend([
                "Schedule regular compliance reviews",
                "Update compliance documentation",
                "Monitor regulatory changes and updates",
                "Maintain current compliance certifications"
            ])
        else:
            recommendations.extend([
                "Continue baseline compliance activities",
                "Monitor for regulatory updates",
                "Maintain compliance documentation"
            ])
        
        return recommendations[:6]  # Focus on essential compliance actions