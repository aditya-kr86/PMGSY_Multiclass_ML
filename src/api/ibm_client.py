"""
IBM Cloud Machine Learning API client.
Handles authentication and prediction requests.
"""

import requests
from typing import Dict, Any, List, Tuple
from ..config import config


class IBMCloudClient:
    """Client for IBM Cloud ML API."""
    
    def __init__(self):
        self.api_key = config.IBM_API_KEY
        self.endpoint = config.get_ml_endpoint()
        self._token: str | None = None
    
    def _get_token(self) -> str:
        """Fetch IAM access token from IBM Cloud."""
        response = requests.post(
            config.IAM_TOKEN_URL,
            data={
                "apikey": self.api_key,
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
            }
        )
        response.raise_for_status()
        return response.json()["access_token"]
    
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send prediction request to IBM Cloud ML.
        
        Args:
            input_data: Dictionary with 'fields' and 'values' keys
            
        Returns:
            API response with predictions
        """
        token = self._get_token()
        
        payload = {"input_data": [input_data]}
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(self.endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
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
        
        Returns:
            Tuple of (predicted_scheme, probabilities, max_confidence)
        """
        input_data = {
            "fields": [
                "STATE_NAME",
                "DISTRICT_NAME",
                "NO_OF_ROAD_WORK_SANCTIONED",
                "LENGTH_OF_ROAD_WORK_SANCTIONED",
                "NO_OF_BRIDGES_SANCTIONED",
                "COST_OF_WORKS_SANCTIONED",
                "NO_OF_ROAD_WORKS_COMPLETED",
                "LENGTH_OF_ROAD_WORK_COMPLETED",
                "NO_OF_BRIDGES_COMPLETED",
                "EXPENDITURE_OCCURED",
                "NO_OF_ROAD_WORKS_BALANCE",
                "LENGTH_OF_ROAD_WORK_BALANCE",
                "NO_OF_BRIDGES_BALANCE",
                "COLUMN15"
            ],
            "values": [[
                state,
                district,
                road_sanctioned,
                length_sanctioned,
                bridges_sanctioned,
                cost_sanctioned,
                road_completed,
                length_completed,
                bridges_completed,
                expenditure,
                road_balance,
                length_balance,
                bridges_balance,
                0
            ]]
        }
        
        result = self.predict(input_data)
        
        prediction = result["predictions"][0]["values"][0][0]
        probabilities = result["predictions"][0]["values"][0][1]
        max_confidence = max(probabilities)
        
        return prediction, probabilities, max_confidence


def get_confidence_level(confidence: float) -> Tuple[str, str]:
    """
    Determine confidence level based on probability.
    
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
