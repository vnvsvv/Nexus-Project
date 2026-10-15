import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.config import config
from src.utils.helpers import Logger

logger = Logger.setup()

class NetworkIDS:
    def __init__(self):
        self.model = None
        self.le_protocol = LabelEncoder()
        self.le_label = LabelEncoder()
        self.feature_names = None
    
    def load_data(self, filepath):
        logger.info(f"Loading: {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Shape: {df.shape}")
        return df
    
    def preprocess(self, df):
        logger.info("Preprocessing...")
        df = df.copy()
        df['protocol_encoded'] = self.le_protocol.fit_transform(df['protocol'])
        df['label_encoded'] = self.le_label.fit_transform(df['label'])
        
        self.feature_names = ['src_port', 'dst_port', 'packet_length', 'packet_count', 'duration', 'protocol_encoded']
        X = df[self.feature_names].fillna(0)
        y = df['label_encoded']
        
        return X, y, df
    
    def train(self, X, y):
        logger.info("Training model...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        self.model = RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
        self.model.fit(X_train, y_train)
        
        accuracy = self.model.score(X_test, y_test)
        logger.info(f"Accuracy: {accuracy:.4f}")
        
        return self.model, accuracy
    
    def save_model(self, filepath):
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, filepath)
        logger.info(f"Saved: {filepath}")

def main():
    ids = NetworkIDS()
    df = ids.load_data('data/raw/network_traffic.csv')
    X, y, _ = ids.preprocess(df)
    ids.train(X, y)
    ids.save_model('src/models/network_ids_model.pkl')
    logger.info("Done!")

if __name__ == "__main__":
    main()
