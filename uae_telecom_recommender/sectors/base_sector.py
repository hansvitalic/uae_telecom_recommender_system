"""
Base sector module for UAE Telecom Recommender System.
Defines the abstract base class for all sector-specific modules.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import numpy as np
from dataclasses import dataclass


@dataclass
class RiskAssessment:
    """Risk assessment result for a sector."""
    sector_id: str
    risk_level: float  # 0.0 to 1.0
    risk_factors: List[str]
    mitigation_strategies: List[str]
    confidence: float  # 0.0 to 1.0
    timestamp: str


@dataclass
class ProjectData:
    """Project data structure for risk assessment."""
    project_id: str
    sector_id: str
    description: str
    budget: float
    timeline_days: int
    complexity_score: float  # 0.0 to 1.0
    stakeholders: List[str]
    technologies: List[str]
    dependencies: List[str]
    historical_risks: Optional[List[str]] = None


class BaseSector(ABC):
    """Abstract base class for sector-specific risk assessment modules."""
    
    def __init__(self, sector_id: str, config: Dict[str, Any]):
        """Initialize the sector module.
        
        Args:
            sector_id: Unique identifier for the sector
            config: Sector configuration from config manager
        """
        self.sector_id = sector_id
        self.name = config['name']
        self.description = config['description']
        self.risk_factors = config['risk_factors']
        self.weight = config['weight']
        
        # Initialize sector-specific parameters
        self._initialize_parameters()
    
    @abstractmethod
    def _initialize_parameters(self) -> None:
        """Initialize sector-specific parameters and models."""
        pass
    
    @abstractmethod
    def assess_risk(self, project_data: ProjectData) -> RiskAssessment:
        """Assess risk for a project in this sector.
        
        Args:
            project_data: Project information for risk assessment
            
        Returns:
            Risk assessment result
        """
        pass
    
    @abstractmethod
    def get_recommendations(self, risk_assessment: RiskAssessment) -> List[str]:
        """Get recommendations based on risk assessment.
        
        Args:
            risk_assessment: Risk assessment result
            
        Returns:
            List of actionable recommendations
        """
        pass
    
    def calculate_base_risk_score(self, project_data: ProjectData) -> float:
        """Calculate base risk score using common factors.
        
        Args:
            project_data: Project data
            
        Returns:
            Base risk score (0.0 to 1.0)
        """
        # Base factors affecting all sectors
        budget_factor = min(project_data.budget / 1000000, 1.0)  # Normalize to 1M AED
        timeline_factor = min(project_data.timeline_days / 365, 1.0)  # Normalize to 1 year
        complexity_factor = project_data.complexity_score
        dependency_factor = min(len(project_data.dependencies) / 10, 1.0)  # Normalize to 10 deps
        
        # Weight the factors
        base_score = (
            budget_factor * 0.25 +
            timeline_factor * 0.25 +
            complexity_factor * 0.35 +
            dependency_factor * 0.15
        )
        
        return np.clip(base_score, 0.0, 1.0)
    
    def get_common_mitigation_strategies(self) -> List[str]:
        """Get common mitigation strategies applicable to all sectors."""
        return [
            "Regular risk monitoring and assessment",
            "Stakeholder communication and alignment",
            "Contingency planning and backup procedures",
            "Vendor and supplier diversification",
            "Staff training and skill development",
            "Documentation and knowledge management",
            "Quality assurance and testing protocols",
            "Budget reserves for unexpected costs",
            "Timeline buffers for critical activities",
            "Compliance monitoring and reporting"
        ]
    
    def calculate_confidence_score(self, project_data: ProjectData) -> float:
        """Calculate confidence score for the risk assessment.
        
        Args:
            project_data: Project data
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        # Factors that increase confidence in the assessment
        data_completeness = 0.0
        
        # Check data completeness
        if project_data.description:
            data_completeness += 0.2
        if project_data.budget > 0:
            data_completeness += 0.2
        if project_data.timeline_days > 0:
            data_completeness += 0.2
        if project_data.technologies:
            data_completeness += 0.2
        if project_data.historical_risks:
            data_completeness += 0.2
        
        return data_completeness