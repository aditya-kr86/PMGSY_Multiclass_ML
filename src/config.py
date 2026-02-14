"""
Configuration module for PMGSY Scheme Predictor.
Loads environment variables and provides app-wide settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration settings."""
    
    # IBM Cloud credentials
    IBM_API_KEY: str = os.getenv("IBM_API_KEY", "")
    DEPLOYMENT_ID: str = os.getenv("DEPLOYMENT_ID", "")
    IBM_REGION: str = os.getenv("IBM_REGION", "us-south")
    
    # IBM Cloud endpoints
    IAM_TOKEN_URL: str = "https://iam.cloud.ibm.com/identity/token"
    
    @classmethod
    def get_ml_endpoint(cls) -> str:
        """Get the IBM Cloud ML prediction endpoint."""
        return f"https://{cls.IBM_REGION}.ml.cloud.ibm.com/ml/v4/deployments/{cls.DEPLOYMENT_ID}/predictions?version=2021-05-01"
    
    # Data paths
    DATA_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "PMGSY_DATASET.csv")
    
    # Model metrics (hardcoded for display)
    MODEL_ACCURACY: str = "89.4%"
    MODEL_PRECISION: str = "88.7%"
    MODEL_RECALL: str = "87.9%"
    TRAINING_RECORDS: str = "2,190+"
    
    # App settings
    APP_TITLE: str = "PMGSY Scheme Predictor"
    APP_SUBTITLE: str = "AI-powered infrastructure scheme classification using IBM Cloud ML"


# Singleton instance
config = Config()
