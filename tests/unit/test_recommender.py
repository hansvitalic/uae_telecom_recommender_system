"""
Unit tests for the main recommender system.
"""

import pytest
from uae_telecom_recommender.core.recommender import TelecomRecommenderSystem
from uae_telecom_recommender.sectors.base_sector import ProjectData


class TestTelecomRecommenderSystem:
    """Test cases for TelecomRecommenderSystem."""
    
    def test_initialization(self):
        """Test system initialization."""
        recommender = TelecomRecommenderSystem()
        
        assert recommender.config_manager is not None
        assert recommender.risk_manager is not None
        assert recommender.uae_settings is not None
    
    def test_create_sample_projects(self):
        """Test sample project creation."""
        recommender = TelecomRecommenderSystem()
        
        # Test all sample project types
        project_types = ['network_upgrade', 'cybersecurity_enhancement', 'customer_portal']
        
        for project_type in project_types:
            project = recommender.create_sample_project(project_type)
            assert isinstance(project, ProjectData)
            assert project.project_id is not None
            assert project.description is not None
            assert project.budget > 0
            assert project.timeline_days > 0
            assert 0 <= project.complexity_score <= 1
    
    def test_assess_sample_project(self):
        """Test assessment of sample project."""
        recommender = TelecomRecommenderSystem()
        
        # Create and assess a sample project
        project = recommender.create_sample_project('network_upgrade')
        report = recommender.assess_project(project)
        
        assert report is not None
        assert report.project_data == project
        assert 0 <= report.overall_risk <= 1
        assert report.risk_category in ['MINIMAL', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        assert len(report.risk_assessments) > 0
        assert len(report.top_risks) > 0
        assert len(report.priority_recommendations) > 0
    
    def test_sector_information(self):
        """Test getting sector information."""
        recommender = TelecomRecommenderSystem()
        sector_info = recommender.get_sector_information()
        
        assert isinstance(sector_info, dict)
        assert len(sector_info) == 10  # Should have all 10 sectors
        
        # Check that each sector has required info
        for sector_id, info in sector_info.items():
            assert 'name' in info
            assert 'weight' in info
            assert 'description' in info
            assert 'risk_factors' in info
            assert 'implemented' in info
    
    def test_uae_context(self):
        """Test UAE context information."""
        recommender = TelecomRecommenderSystem()
        context = recommender.get_uae_context()
        
        assert 'regulatory_environment' in context
        assert 'risk_tolerance' in context
        assert 'recommendation_engine' in context
        assert 'sectors_overview' in context
        
        # Check regulatory environment
        reg_env = context['regulatory_environment']
        assert 'primary_regulator' in reg_env
        assert 'UAE Telecommunications Regulatory Authority' in reg_env['primary_regulator']
    
    def test_project_validation(self):
        """Test project data validation."""
        recommender = TelecomRecommenderSystem()
        
        # Valid project should pass
        valid_project = ProjectData(
            project_id="TEST_001",
            sector_id="test",
            description="Test project",
            budget=1000000,
            timeline_days=180,
            complexity_score=0.5,
            stakeholders=["Test Team"],
            technologies=["Test Tech"],
            dependencies=["Test Dep"]
        )
        
        report = recommender.assess_project(valid_project)
        assert report is not None
        
        # Invalid project should raise error
        invalid_project = ProjectData(
            project_id="",  # Empty ID
            sector_id="test",
            description="",  # Empty description
            budget=0,  # Zero budget
            timeline_days=0,  # Zero timeline
            complexity_score=1.5,  # Invalid complexity
            stakeholders=[],  # No stakeholders
            technologies=[],  # No technologies
            dependencies=[]
        )
        
        with pytest.raises(ValueError):
            recommender.assess_project(invalid_project)