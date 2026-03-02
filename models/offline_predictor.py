"""
Offline Predictor using locally trained XGBoost model.

This class provides the same interface as IBMCloudClient, making it a
drop-in replacement when IBM Cloud is unavailable.

Usage:
    from models import OfflinePredictor
    
    predictor = OfflinePredictor()
    prediction, probabilities, confidence = predictor.predict_scheme(
        state="Andhra Pradesh",
        district="East Godavari",
        road_sanctioned=100,
        ...
    )
"""

import os
import pickle
from typing import List, Tuple

import pandas as pd
import numpy as np


class OfflinePredictor:
    """
    Offline prediction using locally trained XGBoost model.
    
    Provides the same interface as IBMCloudClient for seamless switching.
    """
    
    def __init__(self):
        """Initialize the offline predictor by loading saved model artifacts."""
        self.model_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(self.model_dir, "pmgsy_xgboost_model.pkl")
        self.encoder_path = os.path.join(self.model_dir, "label_encoder.pkl")
        
        self.pipeline = None
        self.label_encoder = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and label encoder from disk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model not found at {self.model_path}. "
                "Please run 'python -m models.train_xgboost' first."
            )
        
        if not os.path.exists(self.encoder_path):
            raise FileNotFoundError(
                f"Label encoder not found at {self.encoder_path}. "
                "Please run 'python -m models.train_xgboost' first."
            )
        
        # Load pipeline
        with open(self.model_path, 'rb') as f:
            self.pipeline = pickle.load(f)
        
        # Load label encoder
        with open(self.encoder_path, 'rb') as f:
            self.label_encoder = pickle.load(f)
        
        print("✓ Offline model loaded successfully")
    
    @property
    def classes(self) -> List[str]:
        """Get the list of class labels."""
        return list(self.label_encoder.classes_)
    
    def predict_scheme(
        self,
        state: str,
        district: str,
        road_sanctioned: int,
        length_sanctioned: float,
        bridges_sanctioned: int,
        cost_sanctioned: float,
        road_completed: int,
        length_completed: float,
        bridges_completed: int,
        expenditure: float,
        road_balance: int,
        length_balance: float,
        bridges_balance: int
    ) -> Tuple[str, List[float], float]:
        """
        Predict PMGSY scheme for given project details.
        
        This method has the same signature as IBMCloudClient.predict_scheme(),
        making it a drop-in replacement.
        
        Args:
            state: State name
            district: District name
            road_sanctioned: Number of road works sanctioned
            length_sanctioned: Length of road work sanctioned (km)
            bridges_sanctioned: Number of bridges sanctioned
            cost_sanctioned: Cost of works sanctioned (lakhs)
            road_completed: Number of road works completed
            length_completed: Length of road work completed (km)
            bridges_completed: Number of bridges completed
            expenditure: Expenditure occurred (lakhs)
            road_balance: Number of road works balance
            length_balance: Length of road work balance (km)
            bridges_balance: Number of bridges balance
            
        Returns:
            Tuple of (predicted_scheme, probabilities, max_confidence)
        """
        # Create input dataframe matching training format
        input_data = pd.DataFrame({
            "STATE_NAME": [state],
            "DISTRICT_NAME": [district],
            "NO_OF_ROAD_WORK_SANCTIONED": [road_sanctioned],
            "LENGTH_OF_ROAD_WORK_SANCTIONED": [length_sanctioned],
            "NO_OF_BRIDGES_SANCTIONED": [bridges_sanctioned],
            "COST_OF_WORKS_SANCTIONED": [cost_sanctioned],
            "NO_OF_ROAD_WORKS_COMPLETED": [road_completed],
            "LENGTH_OF_ROAD_WORK_COMPLETED": [length_completed],
            "NO_OF_BRIDGES_COMPLETED": [bridges_completed],
            "EXPENDITURE_OCCURED": [expenditure],
            "NO_OF_ROAD_WORKS_BALANCE": [road_balance],
            "LENGTH_OF_ROAD_WORK_BALANCE": [length_balance],
            "NO_OF_BRIDGES_BALANCE": [bridges_balance]
        })
        
        # Get prediction
        prediction_encoded = self.pipeline.predict(input_data)[0]
        probabilities = self.pipeline.predict_proba(input_data)[0]
        
        # Decode prediction
        prediction = self.label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Get max confidence
        max_confidence = float(np.max(probabilities))
        
        # Convert probabilities to list
        probabilities_list = probabilities.tolist()
        
        return prediction, probabilities_list, max_confidence
    
    def predict_batch(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Predict for multiple records at once.
        
        Args:
            data: DataFrame with required columns
            
        Returns:
            DataFrame with predictions and probabilities
        """
        predictions_encoded = self.pipeline.predict(data)
        probabilities = self.pipeline.predict_proba(data)
        
        predictions = self.label_encoder.inverse_transform(predictions_encoded)
        max_confidences = np.max(probabilities, axis=1)
        
        result = data.copy()
        result['predicted_scheme'] = predictions
        result['confidence'] = max_confidences
        
        return result
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        return {
            "model_type": "XGBoost Classifier",
            "classes": self.classes,
            "num_classes": len(self.classes),
            "model_path": self.model_path,
            "is_loaded": self.pipeline is not None
        }


def get_confidence_level(confidence: float) -> Tuple[str, str]:
    """
    Determine confidence level based on probability.
    
    Same function as in ibm_client.py for consistency.
    
    Args:
        confidence: Prediction confidence (0-1)
        
    Returns:
        Tuple of (level_text, css_class)
    """
    if confidence >= 0.80:
        return "HIGH", "high-confidence"
    elif confidence >= 0.60:
        return "MEDIUM", "medium-confidence"
    else:
        return "LOW", "low-confidence"


# Quick test
if __name__ == "__main__":
    print("Testing Offline Predictor...")
    print("-" * 40)
    
    try:
        predictor = OfflinePredictor()
        
        # Test prediction
        prediction, probs, confidence = predictor.predict_scheme(
            state="Andhra Pradesh",
            district="East Godavari",
            road_sanctioned=500,
            length_sanctioned=1200.5,
            bridges_sanctioned=25,
            cost_sanctioned=45000.0,
            road_completed=450,
            length_completed=1100.0,
            bridges_completed=20,
            expenditure=40000.0,
            road_balance=50,
            length_balance=100.5,
            bridges_balance=5
        )
        
        print(f"\n✓ Prediction: {prediction}")
        print(f"✓ Confidence: {confidence:.2%}")
        print(f"✓ All Probabilities: {[f'{p:.2%}' for p in probs]}")
        print(f"✓ Classes: {predictor.classes}")
        
    except FileNotFoundError as e:
        print(f"\n⚠️ {e}")
        print("Run training first: python -m models.train_xgboost")
