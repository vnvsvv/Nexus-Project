import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils.helpers import Logger

logger = Logger.setup()

class RealisticDataGenerator:
    def __init__(self, seed=42):
        np.random.seed(seed)
        self.logger = logger
    
    def generate_brute_force(self, num_records=500):
        """Generate brute force attack data"""
        self.logger.info("Generating Brute Force attacks...")
        
        attacker_ip = "192.168.1.200"  # Single attacker
        target_server = "192.168.1.10"  # Web server
        
        data = {
            'timestamp': [datetime.now() - timedelta(seconds=i) for i in range(num_records)],
            'src_ip': [attacker_ip] * num_records,
            'dst_ip': [target_server] * num_records,
            'src_port': np.random.randint(50000, 65535, num_records),
            'dst_port': [22] * num_records,  # SSH
            'protocol': ['TCP'] * num_records,
            'packet_length': np.random.randint(40, 100, num_records),
            'packet_count': np.random.randint(1, 5, num_records),
            'duration': np.random.exponential(0.5, num_records),
            'label': ['Brute_Force'] * num_records
        }
        
        return pd.DataFrame(data)
    
    def generate_malware(self, num_records=300):
        """Generate malware communication"""
        self.logger.info("Generating Malware traffic...")
        
        infected_ips = [f"192.168.1.{i}" for i in range(100, 110)]
        c2_server = "10.0.0.50"  # Command & Control
        
        data = {
            'timestamp': [datetime.now() - timedelta(seconds=i) for i in range(num_records)],
            'src_ip': np.random.choice(infected_ips, num_records),
            'dst_ip': [c2_server] * num_records,
            'src_port': np.random.randint(50000, 65535, num_records),
            'dst_port': np.random.choice([80, 443, 8080, 53], num_records),
            'protocol': np.random.choice(['TCP', 'UDP'], num_records),
            'packet_length': np.random.exponential(2000, num_records).astype(int),
            'packet_count': np.random.poisson(100, num_records),
            'duration': np.random.exponential(30, num_records),
            'label': ['Malware'] * num_records
        }
        
        return pd.DataFrame(data)
    
    def generate_port_scan(self, num_records=400):
        """Generate port scanning"""
        self.logger.info("Generating Port Scan attacks...")
        
        scanner_ip = "192.168.1.250"
        target_range = [f"192.168.1.{i}" for i in range(30, 40)]
        
        data = {
            'timestamp': [datetime.now() - timedelta(seconds=i) for i in range(num_records)],
            'src_ip': [scanner_ip] * num_records,
            'dst_ip': np.random.choice(target_range, num_records),
            'src_port': np.random.randint(1024, 65535, num_records),
            'dst_port': np.random.randint(1, 1024, num_records),
            'protocol': ['TCP'] * num_records,
            'packet_length': np.random.randint(40, 60, num_records),
            'packet_count': np.random.randint(1, 2, num_records),
            'duration': np.random.exponential(0.1, num_records),
            'label': ['Port_Scan'] * num_records
        }
        
        return pd.DataFrame(data)
    
    def generate_data_exfiltration(self, num_records=250):
        """Generate data exfiltration"""
        self.logger.info("Generating Data Exfiltration...")
        
        insider_ips = [f"192.168.1.{i}" for i in range(50, 60)]
        external_ips = [f"10.{i}.{j}.{k}" for i in range(1, 3) for j in range(1, 5) for k in range(1, 5)]
        
        data = {
            'timestamp': [datetime.now() - timedelta(seconds=i) for i in range(num_records)],
            'src_ip': np.random.choice(insider_ips, num_records),
            'dst_ip': np.random.choice(external_ips, num_records),
            'src_port': np.random.randint(50000, 65535, num_records),
            'dst_port': np.random.choice([80, 443], num_records),
            'protocol': ['TCP'] * num_records,
            'packet_length': np.random.exponential(5000, num_records).astype(int),
            'packet_count': np.random.poisson(500, num_records),
            'duration': np.random.exponential(60, num_records),
            'label': ['Data_Exfiltration'] * num_records
        }
        
        return pd.DataFrame(data)
    
    def generate_normal(self, num_records=3000):
        """Generate normal traffic"""
        self.logger.info("Generating Normal traffic...")
        
        data = {
            'timestamp': [datetime.now() - timedelta(seconds=i) for i in range(num_records)],
            'src_ip': [f"192.168.1.{np.random.randint(50, 200)}" for _ in range(num_records)],
            'dst_ip': np.random.choice(['192.168.1.10', '192.168.1.20', '192.168.1.30'], num_records),
            'src_port': np.random.randint(50000, 65535, num_records),
            'dst_port': np.random.choice([80, 443, 22, 3306], num_records),
            'protocol': np.random.choice(['TCP', 'UDP'], num_records, p=[0.7, 0.3]),
            'packet_length': np.random.exponential(500, num_records).astype(int),
            'packet_count': np.random.poisson(50, num_records),
            'duration': np.random.exponential(10, num_records),
            'label': ['Normal'] * num_records
        }
        
        return pd.DataFrame(data)
    
    def generate_all(self):
        """Generate all attack types"""
        dfs = [
            self.generate_brute_force(500),
            self.generate_malware(300),
            self.generate_port_scan(400),
            self.generate_data_exfiltration(250),
            self.generate_normal(3000)
        ]
        
        combined = pd.concat(dfs, ignore_index=True)
        combined = combined.sample(frac=1).reset_index(drop=True)
        
        self.logger.info(f"Total records: {len(combined)}")
        self.logger.info(f"Attack breakdown:\n{combined['label'].value_counts()}")
        
        return combined
    
    def save(self, df, filepath):
        df.to_csv(filepath, index=False)
        self.logger.info(f"Saved: {filepath}")

def main():
    gen = RealisticDataGenerator()
    df = gen.generate_all()
    gen.save(df, 'data/raw/realistic_network_traffic.csv')
    logger.info("✓ Realistic data generated!")

if __name__ == "__main__":
    main()
