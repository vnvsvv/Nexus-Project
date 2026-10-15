import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import joblib
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.helpers import Logger

logger = Logger.setup()

class LogAnomalyDetector:
    def __init__(self, encoding_dim=32):
        self.model = None
        self.scaler = StandardScaler()
        self.le_event = LabelEncoder()
        self.le_severity = LabelEncoder()
        self.encoding_dim = encoding_dim
    
    def load_data(self, filepath):
        logger.info(f"Loading: {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Shape: {df.shape}")
        return df
    
    def preprocess(self, df):
        logger.info("Preprocessing...")
        df = df.copy()
        df['event_encoded'] = self.le_event.fit_transform(df['event'])
        df['severity_encoded'] = self.le_severity.fit_transform(df['severity'])
        df['success_encoded'] = (df['success'].astype(int)).values
        
        features = ['event_encoded', 'severity_encoded', 'success_encoded']
        X = df[features].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, df
    
    def build_model(self, input_dim):
        logger.info("Building Autoencoder...")
        input_layer = keras.Input(shape=(input_dim,))
        encoded = layers.Dense(self.encoding_dim, activation='relu')(input_layer)
        decoded = layers.Dense(input_dim, activation='sigmoid')(encoded)
        
        self.model = keras.Model(input_layer, decoded)
        self.model.compile(optimizer='adam', loss='mse')
    
    def train(self, X, epochs=50):
        logger.info("Training...")
        X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, X_train, epochs=epochs, batch_size=32, validation_split=0.1, verbose=0)
        loss = self.model.evaluate(X_test, X_test, verbose=0)
        logger.info(f"Loss: {loss:.4f}")
    
    def save_model(self, filepath):
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        self.model.save(filepath)
        logger.info(f"Saved: {filepath}")

def main():
    detector = LogAnomalyDetector()
    df = detector.load_data('data/raw/security_logs.csv')
    X_scaled, _ = detector.preprocess(df)
    detector.build_model(input_dim=X_scaled.shape[1])
    detector.train(X_scaled)
    detector.save_model('src/models/log_anomaly_model.h5')
    logger.info("Done!")

if __name__ == "__main__":
    main()
