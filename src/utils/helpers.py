import logging
from datetime import datetime
from pathlib import Path

class Logger:
    """Custom logger for NEXUS"""
    
    @staticmethod
    def setup(log_dir="logs/"):
        """Setup logging configuration"""
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        log_file = Path(log_dir) / f"nexus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger("NEXUS")

class DataValidator:
    """Validate data quality"""
    
    @staticmethod
    def check_missing_values(df, threshold=0.5):
        """Check for missing values above threshold"""
        missing = df.isnull().sum() / len(df)
        bad_cols = missing[missing > threshold]
        
        if len(bad_cols) > 0:
            print(f"Columns with >{threshold*100}% missing:")
            print(bad_cols)
            return False
        return True
    
    @staticmethod
    def check_duplicates(df):
        """Check for duplicate rows"""
        duplicates = df.duplicated().sum()
        print(f"Duplicate rows: {duplicates}")
        return duplicates == 0

class FeatureExtractor:
    """Extract features from raw data"""
    
    @staticmethod
    def extract_ip_features(ip_column):
        """Extract features from IP addresses"""
        # Placeholder for IP feature extraction
        return {
            'ip_octets': [int(x) for x in ip_column.split('.')]
        }
    
    @staticmethod
    def extract_temporal_features(timestamp_column):
        """Extract temporal features"""
        # Placeholder for temporal feature extraction
        return {
            'hour': timestamp_column.dt.hour,
            'day_of_week': timestamp_column.dt.dayofweek
        }

if __name__ == "__main__":
    logger = Logger.setup()
    logger.info("NEXUS logger initialized")
    print("Helpers module loaded successfully!")
