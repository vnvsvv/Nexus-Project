import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import config
from src.utils.helpers import Logger

logger = Logger.setup()

class SyntheticDataGenerator:
    """Generate synthetic network and log data for testing"""
    
    def __init__(self, num_records=10000, seed=42):
        np.random.seed(seed)
        self.num_records = num_records
        self.logger = logger
    
    def generate_network_traffic(self):
        """Generate synthetic network traffic data"""
        self.logger.info(f"Generating {self.num_records} network records...")
        
        # Source and destination IPs
        sources = [f"192.168.1.{np.random.randint(50, 254)}" for _ in range(self.num_records)]
        destinations = [f"192.168.1.{np.random.randint(10, 30)}" for _ in range(self.num_records)]
        
        # Protocols
        protocols = np.random.choice(['TCP', 'UDP', 'ICMP'], self.num_records, p=[0.6, 0.3, 0.1])
        
        # Ports
        ports = np.random.randint(1, 65535, self.num_records)
        
        # Packet data
        packet_length = np.random.exponential(scale=500, size=self.num_records)
        packet_count = np.random.poisson(lam=50, size=self.num_records)
        
        # Duration
        duration = np.random.exponential(scale=10, size=self.num_records)
        
        # Labels (mostly normal, some attacks)
        labels = np.random.choice(['Normal', 'Brute_Force', 'Malware', 'Anomaly'], 
                                 self.num_records, 
                                 p=[0.85, 0.05, 0.05, 0.05])
        
        df = pd.DataFrame({
            'timestamp': [datetime.now() - timedelta(seconds=int(i)) for i in range(self.num_records)],
            'src_ip': sources,
            'dst_ip': destinations,
            'protocol': protocols,
            'src_port': np.random.randint(1, 65535, self.num_records),
            'dst_port': ports,
            'packet_length': packet_length.astype(int),
            'packet_count': packet_count.astype(int),
            'duration': duration,
            'label': labels
        })
        
        self.logger.info(f"Generated network traffic: {df.shape}")
        return df
    
    def generate_logs(self):
        """Generate synthetic security logs"""
        self.logger.info(f"Generating {self.num_records} log records...")
        
        usernames = [f"user{np.random.randint(1, 50)}" for _ in range(self.num_records)]
        events = np.random.choice(['login', 'logout', 'failed_login', 'file_access', 'privilege_escalation'],
                                 self.num_records,
                                 p=[0.5, 0.2, 0.15, 0.1, 0.05])
        
        sources = [f"192.168.1.{np.random.randint(50, 254)}" for _ in range(self.num_records)]
        
        df = pd.DataFrame({
            'timestamp': [datetime.now() - timedelta(seconds=int(i)) for i in range(self.num_records)],
            'username': usernames,
            'event': events,
            'source_ip': sources,
            'success': np.random.choice([True, False], self.num_records, p=[0.9, 0.1]),
            'severity': np.random.choice(['Low', 'Medium', 'High'], self.num_records, p=[0.6, 0.3, 0.1])
        })
        
        self.logger.info(f"Generated logs: {df.shape}")
        return df
    
    def save_data(self, network_df, logs_df):
        """Save generated data to CSV"""
        output_dir = Path(config.get_data_path())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        network_path = output_dir / 'network_traffic.csv'
        logs_path = output_dir / 'security_logs.csv'
        
        network_df.to_csv(network_path, index=False)
        logs_df.to_csv(logs_path, index=False)
        
        self.logger.info(f"Saved: {network_path}")
        self.logger.info(f"Saved: {logs_path}")

def main():
    generator = SyntheticDataGenerator(num_records=10000)
    
    network_df = generator.generate_network_traffic()
    logs_df = generator.generate_logs()
    
    generator.save_data(network_df, logs_df)
    
    logger.info("✓ Synthetic data generation complete!")
    print("\nDataset Summary:")
    print(f"Network traffic records: {len(network_df)}")
    print(f"Security logs records: {len(logs_df)}")
    print(f"\nNetwork traffic columns: {list(network_df.columns)}")
    print(f"Security logs columns: {list(logs_df.columns)}")

if __name__ == "__main__":
    main()
