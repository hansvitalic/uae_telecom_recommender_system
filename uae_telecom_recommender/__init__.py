"""
UAE Telecom Recommender System
Sector-aware recommender systems for project risk management in UAE telecom infrastructure.
"""

__version__ = "0.1.0"
__author__ = "Hansel Vitalicio"

from .core.recommender import TelecomRecommenderSystem
from .core.risk_manager import RiskManager

__all__ = ["TelecomRecommenderSystem", "RiskManager"]