"""
Main UAE Telecom Recommender System.
Provides comprehensive risk assessment and recommendations for UAE telecom projects.
"""

from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from dataclasses import asdict

from ..config.config_manager import ConfigManager
from .risk_manager import RiskManager
from ..sectors.base_sector import ProjectData, RiskAssessment


class RecommendationReport:
    """Comprehensive recommendation report for a project."""
    
    def __init__(self, project_data: ProjectData, risk_assessments: Dict[str, RiskAssessment],
                 overall_risk: float, top_risks: List[tuple], priority_recommendations: List[tuple]):
        self.project_data = project_data
        self.risk_assessments = risk_assessments
        self.overall_risk = overall_risk
        self.top_risks = top_risks
        self.priority_recommendations = priority_recommendations
        self.generated_at = datetime.now().isoformat()
        self.risk_category = self._categorize_risk(overall_risk)
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk level based on UAE risk tolerance."""
        if risk_score >= 0.8:
            return "CRITICAL"
        elif risk_score >= 0.6:
            return "HIGH"
        elif risk_score >= 0.4:
            return "MEDIUM"
        elif risk_score >= 0.2:
            return "LOW"
        else:
            return "MINIMAL"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary format."""
        return {
            'project_id': self.project_data.project_id,
            'project_description': self.project_data.description,
            'overall_risk_score': round(self.overall_risk, 3),
            'risk_category': self.risk_category,
            'generated_at': self.generated_at,
            'sector_assessments': {
                sector_id: {
                    'risk_level': round(assessment.risk_level, 3),
                    'risk_factors': assessment.risk_factors,
                    'confidence': round(assessment.confidence, 3)
                }
                for sector_id, assessment in self.risk_assessments.items()
            },
            'top_risk_factors': [
                {'factor': risk[0], 'sector': risk[1], 'risk_level': round(risk[2], 3)}
                for risk in self.top_risks
            ],
            'priority_recommendations': [
                {'recommendation': rec[0], 'sector': rec[1], 'risk_level': round(rec[2], 3)}
                for rec in self.priority_recommendations
            ]
        }
    
    def to_json(self) -> str:
        """Convert report to JSON format."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class TelecomRecommenderSystem:
    """Main UAE Telecom Recommender System for risk management."""
    
    def __init__(self, config_path: str = None):
        """Initialize the recommender system.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_manager = ConfigManager(config_path)
        self.config_manager.validate_config()
        self.risk_manager = RiskManager(self.config_manager)
        
        # UAE-specific settings
        self.uae_settings = self.config_manager.get_uae_settings()
        self.recommendation_settings = self.config_manager.get_recommendation_settings()
    
    def assess_project(self, project_data: ProjectData, 
                      sectors_filter: Optional[List[str]] = None) -> RecommendationReport:
        """Conduct comprehensive project risk assessment and generate recommendations.
        
        Args:
            project_data: Project information for assessment
            sectors_filter: Optional list of sector IDs to focus on
            
        Returns:
            Comprehensive recommendation report
        """
        # Validate project data
        validation_issues = self.risk_manager.validate_project_data(project_data)
        if validation_issues:
            raise ValueError(f"Project data validation failed: {'; '.join(validation_issues)}")
        
        # Determine relevant sectors
        relevant_sectors = self._identify_relevant_sectors(project_data, sectors_filter)
        
        # Conduct risk assessments
        risk_assessments = self.risk_manager.assess_project_risk(project_data, relevant_sectors)
        
        # Calculate overall risk
        overall_risk = self.risk_manager.calculate_overall_risk(risk_assessments)
        
        # Get top risks and recommendations
        top_risks = self.risk_manager.get_top_risk_factors(risk_assessments, limit=10)
        priority_recommendations = self.risk_manager.get_priority_recommendations(
            risk_assessments, limit=15
        )
        
        return RecommendationReport(
            project_data=project_data,
            risk_assessments=risk_assessments,
            overall_risk=overall_risk,
            top_risks=top_risks,
            priority_recommendations=priority_recommendations
        )
    
    def _identify_relevant_sectors(self, project_data: ProjectData, 
                                 sectors_filter: Optional[List[str]] = None) -> List[str]:
        """Identify most relevant sectors for a project based on keywords and context.
        
        Args:
            project_data: Project information
            sectors_filter: Optional filter for specific sectors
            
        Returns:
            List of relevant sector IDs
        """
        if sectors_filter:
            return sectors_filter
        
        # Keywords that indicate sector relevance
        sector_keywords = {
            'network_infrastructure': [
                'network', 'infrastructure', 'fiber', 'tower', 'equipment', 
                'hardware', 'connectivity', 'transmission', 'switching'
            ],
            'cybersecurity': [
                'security', 'cybersecurity', 'cyber', 'protection', 'firewall',
                'encryption', 'threat', 'vulnerability', 'incident'
            ],
            'regulatory_compliance': [
                'compliance', 'regulation', 'regulatory', 'license', 'legal',
                'policy', 'audit', 'standard', 'certification'
            ],
            'it_software_development': [
                'software', 'development', 'programming', 'system', 'integration',
                'application', 'platform', 'database', 'api'
            ],
            'telecom_services': [
                'service', 'voice', 'data', 'internet', 'mobile', 'broadband',
                'telecommunication', 'subscriber', 'billing'
            ],
            'customer_service_delivery': [
                'customer', 'support', 'service delivery', 'helpdesk', 'portal',
                'experience', 'satisfaction', 'call center'
            ],
            'supply_chain_management': [
                'procurement', 'vendor', 'supplier', 'logistics', 'inventory',
                'sourcing', 'contract', 'delivery'
            ],
            'marketing_sales': [
                'marketing', 'sales', 'campaign', 'promotion', 'advertising',
                'customer acquisition', 'revenue', 'pricing'
            ],
            'human_resources': [
                'training', 'staff', 'employee', 'recruitment', 'workforce',
                'skills', 'performance', 'human resources'
            ],
            'research_development': [
                'research', 'development', 'innovation', 'r&d', 'prototype',
                'pilot', 'testing', 'experiment', 'technology development'
            ]
        }
        
        relevant_sectors = []
        description_lower = project_data.description.lower()
        
        # Check each sector for keyword matches
        for sector_id, keywords in sector_keywords.items():
            relevance_score = 0
            for keyword in keywords:
                if keyword in description_lower:
                    relevance_score += 1
            
            # Also check technologies
            for tech in project_data.technologies:
                tech_lower = tech.lower()
                for keyword in keywords:
                    if keyword in tech_lower:
                        relevance_score += 1
            
            if relevance_score > 0:
                relevant_sectors.append((sector_id, relevance_score))
        
        # Sort by relevance and return sector IDs
        relevant_sectors.sort(key=lambda x: x[1], reverse=True)
        
        # Always include top 3 sectors plus any with high relevance
        result = [sector[0] for sector in relevant_sectors[:3]]
        for sector_id, score in relevant_sectors[3:]:
            if score >= 3:  # High relevance threshold
                result.append(sector_id)
        
        # Ensure we always assess key sectors
        mandatory_sectors = ['cybersecurity', 'regulatory_compliance']
        for sector in mandatory_sectors:
            if sector not in result:
                result.append(sector)
        
        return result
    
    def get_sector_information(self) -> Dict[str, Any]:
        """Get information about all available sectors.
        
        Returns:
            Dictionary with sector information and capabilities
        """
        sector_info = self.risk_manager.get_sector_summary()
        
        # Add UAE-specific context
        for sector_id, info in sector_info.items():
            sector_config = self.config_manager.get_sector(sector_id)
            info.update({
                'description': sector_config['description'],
                'risk_factors': sector_config['risk_factors'],
                'uae_context': True
            })
        
        return sector_info
    
    def create_sample_project(self, project_type: str = "network_upgrade") -> ProjectData:
        """Create a sample project for demonstration purposes.
        
        Args:
            project_type: Type of sample project to create
            
        Returns:
            Sample project data
        """
        sample_projects = {
            "network_upgrade": ProjectData(
                project_id="UAE_NET_2024_001",
                sector_id="network_infrastructure",
                description="5G network infrastructure upgrade across Dubai and Abu Dhabi, including new cell towers, fiber optic cables, and core network equipment replacement",
                budget=75000000,  # 75M AED
                timeline_days=548,  # 18 months
                complexity_score=0.8,
                stakeholders=["Etisalat", "du", "UAE Ministry of Energy", "Dubai Municipality", "Abu Dhabi Government"],
                technologies=["5G NR", "Fiber Optic", "Massive MIMO", "Network Function Virtualization", "Edge Computing"],
                dependencies=["Spectrum allocation", "Site permits", "Environmental approvals", "Vendor contracts"]
            ),
            "cybersecurity_enhancement": ProjectData(
                project_id="UAE_SEC_2024_002",
                sector_id="cybersecurity",
                description="Comprehensive cybersecurity enhancement for critical telecom infrastructure including AI-powered threat detection, zero-trust architecture, and compliance with UAE Cyber Security Law",
                budget=25000000,  # 25M AED
                timeline_days=365,  # 12 months
                complexity_score=0.7,
                stakeholders=["UAE Cyber Security Council", "Telecom operators", "Critical infrastructure providers"],
                technologies=["AI-powered security", "Zero-trust architecture", "SIEM", "Threat intelligence", "Endpoint protection"],
                dependencies=["Security clearances", "Compliance audits", "Staff training", "Vendor assessments"]
            ),
            "customer_portal": ProjectData(
                project_id="UAE_CUS_2024_003",
                sector_id="customer_service_delivery",
                description="Digital customer self-service portal with AI chatbot, mobile app, and integrated billing system for improved customer experience",
                budget=15000000,  # 15M AED
                timeline_days=273,  # 9 months
                complexity_score=0.6,
                stakeholders=["Customer service teams", "IT development", "Marketing", "Billing department"],
                technologies=["React Native", "AI Chatbot", "Cloud services", "API Gateway", "Analytics platform"],
                dependencies=["Customer data migration", "Payment gateway integration", "App store approvals", "User testing"]
            )
        }
        
        if project_type not in sample_projects:
            raise ValueError(f"Unknown project type: {project_type}. Available: {list(sample_projects.keys())}")
        
        return sample_projects[project_type]
    
    def get_uae_context(self) -> Dict[str, Any]:
        """Get UAE-specific regulatory and business context.
        
        Returns:
            UAE telecom context information
        """
        return {
            'regulatory_environment': {
                'primary_regulator': self.uae_settings['regulatory_authority'],
                'key_laws': self.uae_settings['compliance_frameworks'],
                'emergency_contacts': self.uae_settings['emergency_contact_authorities']
            },
            'risk_tolerance': self.uae_settings['risk_tolerance_levels'],
            'recommendation_engine': self.recommendation_settings,
            'sectors_overview': {
                sector_id: {
                    'name': config['name'],
                    'weight': config['weight'],
                    'description': config['description']
                }
                for sector_id, config in self.config_manager.get_sectors().items()
            }
        }