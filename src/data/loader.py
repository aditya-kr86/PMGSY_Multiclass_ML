"""
Data loading utilities for PMGSY dataset.
"""

import pandas as pd
from typing import List, Dict, Any
from functools import lru_cache


class DataLoader:
    """Handles loading and processing of PMGSY dataset."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self._df: pd.DataFrame | None = None
    
    @property
    def df(self) -> pd.DataFrame:
        """Lazy load and cache the dataset."""
        if self._df is None:
            self._df = pd.read_csv(self.data_path)
            self._df.columns = self._df.columns.str.strip()
        return self._df
    
    def get_states(self) -> List[str]:
        """Get sorted list of unique states."""
        return sorted(self.df["STATE_NAME"].dropna().unique().tolist())
    
    def get_districts(self, state: str) -> List[str]:
        """Get sorted list of districts for a given state."""
        return sorted(
            self.df[self.df["STATE_NAME"] == state]["DISTRICT_NAME"]
            .dropna()
            .unique()
            .tolist()
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get dataset statistics for display."""
        return {
            "total_records": len(self.df),
            "total_states": self.df["STATE_NAME"].nunique(),
            "total_districts": self.df["DISTRICT_NAME"].nunique(),
            "total_schemes": self.df["PMGSY_SCHEME"].nunique()
        }


@lru_cache(maxsize=1)
def load_data(data_path: str) -> DataLoader:
    """
    Factory function to create and cache DataLoader instance.
    
    Args:
        data_path: Path to CSV file
        
    Returns:
        Cached DataLoader instance
    """
    return DataLoader(data_path)
