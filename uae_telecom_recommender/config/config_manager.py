"""
Configuration manager for UAE Telecom Recommender System.
"""

import os
import yaml
from typing import Dict, Any, List
from pathlib import Path


class ConfigManager:
    """Manages configuration settings for the UAE Telecom Recommender System."""
    
    def __init__(self, config_path: str = None):
        """Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file. If None, uses default.
        """
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), 
                "sectors_config.yaml"
            )
        
        self.config_path = config_path
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}")
    
    def get_sectors(self) -> Dict[str, Any]:
        """Get all sector configurations."""
        return self._config.get('sectors', {})
    
    def get_sector(self, sector_id: str) -> Dict[str, Any]:
        """Get configuration for a specific sector.
        
        Args:
            sector_id: Sector identifier
            
        Returns:
            Sector configuration dictionary
        """
        sectors = self.get_sectors()
        if sector_id not in sectors:
            raise ValueError(f"Unknown sector: {sector_id}")
        return sectors[sector_id]
    
    def get_sector_names(self) -> List[str]:
        """Get list of all sector names."""
        return [config['name'] for config in self.get_sectors().values()]
    
    def get_sector_weights(self) -> Dict[str, float]:
        """Get sector weights for risk assessment."""
        return {
            sector_id: config['weight']
            for sector_id, config in self.get_sectors().items()
        }
    
    def get_uae_settings(self) -> Dict[str, Any]:
        """Get UAE-specific settings."""
        return self._config.get('uae_settings', {})
    
    def get_recommendation_settings(self) -> Dict[str, Any]:
        """Get recommendation engine settings."""
        return self._config.get('recommendation_engine', {})
    
    def get_risk_factors(self, sector_id: str) -> List[str]:
        """Get risk factors for a specific sector.
        
        Args:
            sector_id: Sector identifier
            
        Returns:
            List of risk factors for the sector
        """
        sector_config = self.get_sector(sector_id)
        return sector_config.get('risk_factors', [])
    
    def get_all_risk_factors(self) -> Dict[str, List[str]]:
        """Get all risk factors grouped by sector."""
        return {
            sector_id: config['risk_factors']
            for sector_id, config in self.get_sectors().items()
        }
    
    def validate_config(self) -> bool:
        """Validate the configuration structure and values.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        # Check if all required sections exist
        required_sections = ['sectors', 'uae_settings', 'recommendation_engine']
        for section in required_sections:
            if section not in self._config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate sector weights sum to approximately 1.0
        total_weight = sum(self.get_sector_weights().values())
        if not (0.95 <= total_weight <= 1.05):  # Allow small floating point errors
            raise ValueError(f"Sector weights sum to {total_weight}, should be close to 1.0")
        
        # Check that each sector has required fields
        required_sector_fields = ['name', 'description', 'risk_factors', 'weight']
        for sector_id, config in self.get_sectors().items():
            for field in required_sector_fields:
                if field not in config:
                    raise ValueError(f"Sector {sector_id} missing required field: {field}")
        
        return True