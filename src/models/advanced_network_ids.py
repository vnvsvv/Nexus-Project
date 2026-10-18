import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
import joblib
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.utils.helpers import Logger

logger = Logger.setup()

class AdvancedNetworkIDS:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.le_protocol = LabelEncoder()
        self.le_label = LabelEncoder()
    
    def load_data(self, filepath):
        logger.info(f"Loading: {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Shape: {df.shape}")
        logger.info(f"Classes: {df['label'].value_counts()}")
        return df
    
    def preprocess(self, df):
        logger.info("Preprocessing...")
        df = df.copy()
        
        df['protocol_encoded'] = self.le_protocol.fit_transform(df['protocol'])
        df['label_encoded'] = self.le_label.fit_transform(df['label'])
        
        features = ['src_port', 'dst_port', 'packet_length', 'packet_count', 'duration', 'protocol_encoded']
        X = df[features].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        y = df['label_encoded']
        
        logger.info(f"Features: {features}")
        logger.info(f"Classes: {self.le_label.classes_}")
        
        return X_scaled, y, df
    
    def train(self, X, y, test_size=0.2):
        logger.info("Training Advanced Network IDS...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Gradient Boosting (better than Random Forest)
        self.model = GradientBoostingClassifier(
            n_estimators=200,
            max_depth=10,
            learning_rate=0.1,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        logger.info("Training complete!")
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"\n=== Results ===")
        logger.info(f"Accuracy: {accuracy:.4f}")
        logger.info(f"\n{classification_report(y_test, y_pred, target_names=self.le_label.classes_)}")
        
        return self.model, accuracy
    
    def save_model(self, filepath):
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, filepath)
        joblib.dump(self.scaler, filepath.replace('.pkl', '_scaler.pkl'))
        logger.info(f"Saved: {filepath}")

def main():
    ids = AdvancedNetworkIDS()
    df = ids.load_data('data/raw/realistic_network_traffic.csv')
    X, y, _ = ids.preprocess(df)
    ids.train(X, y)
    ids.save_model('src/models/advanced_network_ids.pkl')
    logger.info("✓ Advanced IDS ready!")

if __name__ == "__main__":
    main()
