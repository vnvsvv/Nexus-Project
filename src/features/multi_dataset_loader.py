import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.utils.helpers import Logger

logger = Logger.setup()

class MultiDatasetLoader:
    def __init__(self):
        self.datasets = {}
        self.combined = None
    
    def load_csv(self, name, filepath):
        logger.info(f"Loading {name}...")
        df = pd.read_csv(filepath)
        logger.info(f"{name}: {df.shape}")
        self.datasets[name] = df
        return df
    
    def combine(self):
        logger.info("Combining datasets...")
        dfs = []
        for name, df in self.datasets.items():
            dfs.append(df)
        self.combined = pd.concat(dfs, ignore_index=True)
        logger.info(f"Combined: {self.combined.shape}")
        return self.combined
    
    def save_combined(self, filepath):
        self.combined.to_csv(filepath, index=False)
        logger.info(f"Saved: {filepath}")

if __name__ == "__main__":
    loader = MultiDatasetLoader()
    print("Loader ready!")
