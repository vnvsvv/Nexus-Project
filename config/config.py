import yaml
import os
from pathlib import Path

class Config:
    def __init__(self, config_path="config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key, default=None):
        """Get config value by dot notation: 'company.name'"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def get_company_name(self):
        return self.get('company.name')
    
    def get_network_cidr(self):
        return self.get('company.network.cidr')
    
    def get_data_path(self):
        return self.get('data.raw_path')
    
    def get_processed_data_path(self):
        return self.get('data.processed_path')
    
    def __repr__(self):
        return f"Config({self.config_path})"

# Initialize global config
config = Config()

if __name__ == "__main__":
    print("Configuration loaded successfully!")
    print(f"Company: {config.get_company_name()}")
    print(f"Network: {config.get_network_cidr()}")
