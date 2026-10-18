import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.utils.helpers import Logger

logger = Logger.setup()

class AlertCorrelationEngine:
    def __init__(self, time_window_seconds=300):
        self.time_window = time_window_seconds
        self.alerts = []
    
    def add_network_alert(self, src_ip, dst_ip, alert_type, confidence):
        """Add network IDS alert"""
        alert = {
            'timestamp': datetime.now(),
            'source': 'Network_IDS',
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'type': alert_type,
            'confidence': confidence
        }
        self.alerts.append(alert)
        logger.info(f"Network alert: {src_ip} -> {dst_ip}: {alert_type}")
    
    def add_log_alert(self, username, event, severity):
        """Add log anomaly alert"""
        alert = {
            'timestamp': datetime.now(),
            'source': 'Log_Anomaly',
            'username': username,
            'event': event,
            'severity': severity
        }
        self.alerts.append(alert)
        logger.info(f"Log alert: {username}: {event}")
    
    def correlate(self):
        """Correlate related alerts"""
        logger.info("Correlating alerts...")
        correlated = []
        
        for i, alert1 in enumerate(self.alerts):
            for alert2 in self.alerts[i+1:]:
                time_diff = abs((alert1['timestamp'] - alert2['timestamp']).total_seconds())
                
                if time_diff <= self.time_window:
                    if alert1.get('src_ip') == alert2.get('src_ip'):
                        correlated.append({
                            'alert1': alert1['type'],
                            'alert2': alert2.get('event'),
                            'source_ip': alert1.get('src_ip'),
                            'time_diff': time_diff,
                            'correlation_strength': 'HIGH'
                        })
        
        logger.info(f"Correlated {len(correlated)} alert pairs")
        return correlated

class RiskScoringEngine:
    def __init__(self):
        self.weights = {
            'network': 0.25,
            'logs': 0.25,
            'threat_intel': 0.50
        }
    
    def calculate_risk(self, network_score, log_score, threat_score):
        """Calculate weighted risk score"""
        risk = (network_score * self.weights['network'] +
                log_score * self.weights['logs'] +
                threat_score * self.weights['threat_intel'])
        
        return min(1.0, risk)
    
    def classify(self, risk_score):
        """Classify severity"""
        if risk_score >= 0.8:
            return "CRITICAL"
        elif risk_score >= 0.6:
            return "HIGH"
        elif risk_score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def generate_incident(self, src_ip, alert_type, risk_score):
        """Generate incident report"""
        severity = self.classify(risk_score)
        
        incident = {
            'timestamp': datetime.now(),
            'source_ip': src_ip,
            'attack_type': alert_type,
            'risk_score': risk_score,
            'severity': severity,
            'status': 'OPEN'
        }
        
        logger.info(f"Incident created: {src_ip} - {severity} - {risk_score:.2f}")
        return incident

def main():
    # Test correlation
    correlation = AlertCorrelationEngine()
    correlation.add_network_alert('192.168.1.200', '192.168.1.10', 'Brute_Force', 0.95)
    correlation.add_log_alert('admin', 'failed_login', 'HIGH')
    correlated = correlation.correlate()
    
    # Test risk scoring
    risk = RiskScoringEngine()
    score = risk.calculate_risk(0.9, 0.8, 0.7)
    severity = risk.classify(score)
    incident = risk.generate_incident('192.168.1.200', 'Brute_Force', score)
    
    logger.info(f"✓ Risk Score: {score:.2f} - Severity: {severity}")

if __name__ == "__main__":
    main()
