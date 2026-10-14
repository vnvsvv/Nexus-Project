import pandas as pd
import numpy as np
import os
from pathlib import Path

class DataLoader:
    """Load and manage datasets for NEXUS project"""
    
    def __init__(self, data_path="data/raw/"):
        self.data_path = Path(data_path)
        self.raw_data = None
        self.processed_data = None
    
    def load_csv(self, filename):
        """Load CSV file from raw data directory"""
        filepath = self.data_path / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        print(f"Loading: {filename}")
        self.raw_data = pd.read_csv(filepath)
        print(f"Shape: {self.raw_data.shape}")
        print(f"Columns: {list(self.raw_data.columns)}")
        
        return self.raw_data
    
    def get_info(self):
        """Display dataset info"""
        if self.raw_data is None:
            print("No data loaded yet!")
            return
        
        print("\n=== Dataset Info ===")
        print(f"Shape: {self.raw_data.shape}")
        print(f"Columns: {self.raw_data.columns.tolist()}")
        print(f"Dtypes:\n{self.raw_data.dtypes}")
        print(f"Missing values:\n{self.raw_data.isnull().sum()}")
    
    def preprocess(self, drop_na=True, normalize=False):
        """Preprocess dataset"""
        if self.raw_data is None:
            raise ValueError("No data loaded!")
        
        print("Preprocessing...")
        self.processed_data = self.raw_data.copy()
        
        if drop_na:
            initial_rows = len(self.processed_data)
            self.processed_data = self.processed_data.dropna()
            print(f"Dropped {initial_rows - len(self.processed_data)} rows with NA")
        
        if normalize:
            numeric_cols = self.processed_data.select_dtypes(include=[np.number]).columns
            self.processed_data[numeric_cols] = (self.processed_data[numeric_cols] - 
                                                 self.processed_data[numeric_cols].mean()) / \
                                                self.processed_data[numeric_cols].std()
            print(f"Normalized {len(numeric_cols)} numeric columns")
        
        return self.processed_data
    
    def save_processed(self, filename, path="data/processed/"):
        """Save processed data"""
        if self.processed_data is None:
            raise ValueError("No processed data to save!")
        
        output_dir = Path(path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / filename
        self.processed_data.to_csv(filepath, index=False)
        print(f"Saved: {filepath}")

if __name__ == "__main__":
    loader = DataLoader()
    print("DataLoader initialized successfully!")
