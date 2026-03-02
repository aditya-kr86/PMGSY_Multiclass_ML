"""
Offline Model Package

Contains XGBoost training scripts and offline predictor for backup when
IBM Cloud ML is unavailable.
"""

from .offline_predictor import OfflinePredictor

__all__ = ['OfflinePredictor']
