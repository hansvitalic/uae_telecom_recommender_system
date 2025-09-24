"""
Core Risk Manager for UAE Telecom Recommender System.
Manages risk assessments across all sectors.
"""

from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime
from ..config.config_manager import ConfigManager
from ..sectors.base_sector import RiskAssessment, ProjectData
from ..sectors.network_infrastructure import NetworkInfrastructureSector
from ..sectors.cybersecurity import CybersecuritySector
from ..sectors.regulatory_compliance import RegulatoryComplianceSector


class RiskManager:
    """Central risk management system for UAE telecom projects."""
    
    def __init__(self, config_manager: ConfigManager = None):
        """Initialize the risk manager.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager or ConfigManager()
        self.sectors = {}
        self._initialize_sectors()
        
    def _initialize_sectors(self) -> None:
        """Initialize all sector risk assessment modules."""
        sector_configs = self.config_manager.get_sectors()
        
        # Initialize implemented sector modules
        sector_classes = {
            'network_infrastructure': NetworkInfrastructureSector,
            'cybersecurity': CybersecuritySector,
            'regulatory_compliance': RegulatoryComplianceSector
        }
        
        for sector_id, sector_config in sector_configs.items():
            if sector_id in sector_classes:
                self.sectors[sector_id] = sector_classes[sector_id](sector_id, sector_config)
            else:
                # Create placeholder for unimplemented sectors
                self.sectors[sector_id] = self._create_placeholder_sector(sector_id, sector_config)
    
    def _create_placeholder_sector(self, sector_id: str, config: Dict[str, Any]):
        """Create a placeholder sector for future implementation."""
        class PlaceholderSector:
            def __init__(self, sector_id, config):
                self.sector_id = sector_id
                self.name = config['name']
                self.weight = config['weight']
                self.risk_factors = config['risk_factors']
            
            def assess_risk(self, project_data: ProjectData) -> RiskAssessment:
                # Simple placeholder assessment based on project complexity
                base_risk = min(project_data.complexity_score * 0.8, 1.0)
                
                return RiskAssessment(
                    sector_id=self.sector_id,
                    risk_level=base_risk,
                    risk_factors=self.risk_factors[:3],  # First 3 risk factors
                    mitigation_strategies=[
                        f"Conduct {self.name.lower()} risk assessment",
                        f"Implement {self.name.lower()} best practices",
                        f"Monitor {self.name.lower()} key metrics"
                    ],
                    confidence=0.5,  # Lower confidence for placeholder
                    timestamp=datetime.now().isoformat()
                )
            
            def get_recommendations(self, risk_assessment: RiskAssessment) -> List[str]:
                return [
                    f"Develop comprehensive {self.name.lower()} strategy",
                    f"Implement {self.name.lower()} monitoring",
                    f"Regular {self.name.lower()} reviews"
                ]
        
        return PlaceholderSector(sector_id, config)
    
    def assess_project_risk(self, project_data: ProjectData, 
                          sectors_to_assess: Optional[List[str]] = None) -> Dict[str, RiskAssessment]:
        """Assess risk across all relevant sectors for a project.
        
        Args:
            project_data: Project information for risk assessment
            sectors_to_assess: List of sector IDs to assess. If None, assesses all sectors.
            
        Returns:
            Dictionary mapping sector IDs to risk assessments
        """
        if sectors_to_assess is None:
            sectors_to_assess = list(self.sectors.keys())
        
        risk_assessments = {}
        
        for sector_id in sectors_to_assess:
            if sector_id in self.sectors:
                try:
                    risk_assessment = self.sectors[sector_id].assess_risk(project_data)
                    risk_assessments[sector_id] = risk_assessment
                except Exception as e:
                    # Log error and create fallback assessment
                    print(f"Error assessing risk for sector {sector_id}: {e}")
                    risk_assessments[sector_id] = self._create_fallback_assessment(
                        sector_id, project_data, str(e)
                    )
        
        return risk_assessments
    
    def _create_fallback_assessment(self, sector_id: str, project_data: ProjectData, 
                                  error_msg: str) -> RiskAssessment:
        """Create a fallback risk assessment when sector assessment fails."""
        sector = self.sectors.get(sector_id)
        if not sector:
            return None
        
        return RiskAssessment(
            sector_id=sector_id,
            risk_level=0.5,  # Medium risk as fallback
            risk_factors=["Assessment error occurred"],
            mitigation_strategies=[
                f"Review {sector.name} assessment methodology",
                "Conduct manual risk evaluation",
                "Seek expert consultation"
            ],
            confidence=0.1,  # Very low confidence due to error
            timestamp=datetime.now().isoformat()
        )
    
    def calculate_overall_risk(self, risk_assessments: Dict[str, RiskAssessment]) -> float:
        """Calculate overall project risk score weighted by sector importance.
        
        Args:
            risk_assessments: Dictionary of risk assessments by sector
            
        Returns:
            Overall risk score (0.0 to 1.0)
        """
        if not risk_assessments:
            return 0.5  # Medium risk if no assessments
        
        weighted_risk = 0.0
        total_weight = 0.0
        
        for sector_id, assessment in risk_assessments.items():
            if sector_id in self.sectors:
                sector_weight = self.sectors[sector_id].weight
                weighted_risk += assessment.risk_level * sector_weight
                total_weight += sector_weight
        
        if total_weight > 0:
            return min(weighted_risk / total_weight, 1.0)
        else:
            return 0.5
    
    def get_top_risk_factors(self, risk_assessments: Dict[str, RiskAssessment], 
                           limit: int = 10) -> List[tuple]:
        """Get top risk factors across all sectors.
        
        Args:
            risk_assessments: Dictionary of risk assessments by sector
            limit: Maximum number of risk factors to return
            
        Returns:
            List of (risk_factor, sector_name, risk_level) tuples
        """
        all_risks = []
        
        for sector_id, assessment in risk_assessments.items():
            if sector_id in self.sectors:
                sector_name = self.sectors[sector_id].name
                for risk_factor in assessment.risk_factors:
                    all_risks.append((risk_factor, sector_name, assessment.risk_level))
        
        # Sort by risk level and return top risks
        all_risks.sort(key=lambda x: x[2], reverse=True)
        return all_risks[:limit]
    
    def get_priority_recommendations(self, risk_assessments: Dict[str, RiskAssessment],
                                   limit: int = 15) -> List[tuple]:
        """Get priority recommendations across all sectors.
        
        Args:
            risk_assessments: Dictionary of risk assessments by sector
            limit: Maximum number of recommendations to return
            
        Returns:
            List of (recommendation, sector_name, risk_level) tuples
        """
        all_recommendations = []
        
        for sector_id, assessment in risk_assessments.items():
            if sector_id in self.sectors:
                sector = self.sectors[sector_id]
                sector_recommendations = sector.get_recommendations(assessment)
                
                for recommendation in sector_recommendations:
                    all_recommendations.append((
                        recommendation, 
                        sector.name, 
                        assessment.risk_level
                    ))
        
        # Sort by risk level to prioritize high-risk recommendations
        all_recommendations.sort(key=lambda x: x[2], reverse=True)
        return all_recommendations[:limit]
    
    def get_sector_summary(self) -> Dict[str, Any]:
        """Get summary of all available sectors.
        
        Returns:
            Dictionary with sector information
        """
        summary = {}
        
        for sector_id, sector in self.sectors.items():
            summary[sector_id] = {
                'name': sector.name,
                'weight': sector.weight,
                'risk_factors_count': len(sector.risk_factors) if hasattr(sector, 'risk_factors') else 0,
                'implemented': hasattr(sector, 'assess_risk') and callable(sector.assess_risk)
            }
        
        return summary
    
    def validate_project_data(self, project_data: ProjectData) -> List[str]:
        """Validate project data and return list of issues.
        
        Args:
            project_data: Project data to validate
            
        Returns:
            List of validation issues (empty if valid)
        """
        issues = []
        
        if not project_data.project_id:
            issues.append("Project ID is required")
        
        if not project_data.description:
            issues.append("Project description is required")
        
        if project_data.budget <= 0:
            issues.append("Project budget must be greater than 0")
        
        if project_data.timeline_days <= 0:
            issues.append("Project timeline must be greater than 0 days")
        
        if not (0.0 <= project_data.complexity_score <= 1.0):
            issues.append("Complexity score must be between 0.0 and 1.0")
        
        if not project_data.technologies:
            issues.append("At least one technology should be specified")
        
        if not project_data.stakeholders:
            issues.append("At least one stakeholder should be specified")
        
        return issues