"""
Unit tests for configuration management.
"""

import pytest
import os
from uae_telecom_recommender.config.config_manager import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager."""
    
    def test_load_default_config(self):
        """Test loading default configuration."""
        config = ConfigManager()
        
        # Test basic structure
        assert config.get_sectors() is not None
        assert config.get_uae_settings() is not None
        assert config.get_recommendation_settings() is not None
    
    def test_get_sectors(self):
        """Test getting sector configurations."""
        config = ConfigManager()
        sectors = config.get_sectors()
        
        # Should have all 10 sectors
        expected_sectors = [
            'network_infrastructure',
            'it_software_development', 
            'telecom_services',
            'customer_service_delivery',
            'regulatory_compliance',
            'supply_chain_management',
            'cybersecurity',
            'marketing_sales',
            'human_resources',
            'research_development'
        ]
        
        for sector in expected_sectors:
            assert sector in sectors
        
        # Each sector should have required fields
        for sector_id, sector_config in sectors.items():
            assert 'name' in sector_config
            assert 'description' in sector_config
            assert 'risk_factors' in sector_config
            assert 'weight' in sector_config
            assert isinstance(sector_config['risk_factors'], list)
            assert isinstance(sector_config['weight'], (int, float))
    
    def test_get_sector_weights(self):
        """Test getting sector weights."""
        config = ConfigManager()
        weights = config.get_sector_weights()
        
        # Weights should sum to approximately 1.0
        total_weight = sum(weights.values())
        assert 0.95 <= total_weight <= 1.05
        
        # All weights should be positive
        for weight in weights.values():
            assert weight > 0
    
    def test_get_risk_factors(self):
        """Test getting risk factors for sectors."""
        config = ConfigManager()
        
        # Test specific sector
        cyber_risks = config.get_risk_factors('cybersecurity')
        assert isinstance(cyber_risks, list)
        assert len(cyber_risks) > 0
        assert 'Cyber attacks' in cyber_risks
    
    def test_validate_config(self):
        """Test configuration validation."""
        config = ConfigManager()
        
        # Should pass validation
        assert config.validate_config() is True