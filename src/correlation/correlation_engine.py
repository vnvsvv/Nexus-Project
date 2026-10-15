import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.helpers import Logger

logger = Logger.setup()

class CorrelationEngine:
    """Correlate alerts from multiple detection sources"""
    
    def __init__(self, window_seconds=300):
        self.window_seconds = window_seconds
    
    def correlate_alerts(self, network_alerts, log_alerts):
        """Correlate network and log alerts within time window"""
        logger.info("Correlating alerts...")
        
        correlated = []
        
        for idx, net_alert in network_alerts.iterrows():
            # Find matching log alerts within time window
            time_diff = abs((log_alerts['timestamp'] - net_alert['timestamp']).dt.total_seconds())
            matching = log_alerts[time_diff <= self.window_seconds]
            
            if len(matching) > 0:
                correlated.append({
                    'network_src': net_alert['src_ip'],
                    'network_label': net_alert['label'],
                    'log_events': matching['event'].tolist(),
                    'severity': matching['severity'].max(),
                    'correlation_count': len(matching)
                })
        
        logger.info(f"Correlated {len(correlated)} alerts")
        return pd.DataFrame(correlated)
    
    def generate_incident_report(self, correlated_alerts):
        """Generate incident report from correlated alerts"""
        logger.info("Generating incident report...")
        
        report = {
            'total_incidents': len(correlated_alerts),
            'high_severity': len(correlated_alerts[correlated_alerts['severity'] == 'High']),
            'sources': correlated_alerts['network_src'].nunique(),
            'top_events': correlated_alerts['log_events'].explode().value_counts().head(5)
        }
        
        return report

class RiskScorer:
    """Calculate risk score based on multiple factors"""
    
    def __init__(self, network_weight=0.25, log_weight=0.25, threat_weight=0.50):
        self.network_weight = network_weight
        self.log_weight = log_weight
        self.threat_weight = threat_weight
    
    def calculate_risk(self, network_score, log_score, threat_score):
        """Calculate weighted risk score"""
        risk = (network_score * self.network_weight +
                log_score * self.log_weight +
                threat_score * self.threat_weight)
        
        return min(1.0, risk)
    
    def classify_severity(self, risk_score):
        """Classify severity based on risk score"""
        if risk_score >= 0.8:
            return "CRITICAL"
        elif risk_score >= 0.6:
            return "HIGH"
        elif risk_score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"

def main():
    logger.info("Correlation Engine and Risk Scorer initialized")

if __name__ == "__main__":
    main()
