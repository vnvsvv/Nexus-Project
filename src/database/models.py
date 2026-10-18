from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class NetworkAlert(db.Model):
    __tablename__ = 'network_alerts'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    src_ip = db.Column(db.String(15), nullable=False)
    dst_ip = db.Column(db.String(15), nullable=False)
    src_port = db.Column(db.Integer)
    dst_port = db.Column(db.Integer)
    protocol = db.Column(db.String(10))
    alert_type = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float)
    status = db.Column(db.String(20), default='OPEN')
    
    def to_dict(self):
        return {'id': self.id, 'src_ip': self.src_ip, 'dst_ip': self.dst_ip, 'alert_type': self.alert_type, 'confidence': self.confidence}

class Incident(db.Model):
    __tablename__ = 'incidents'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    source_ip = db.Column(db.String(15), nullable=False)
    attack_type = db.Column(db.String(100), nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='OPEN')
    
    def to_dict(self):
        return {'id': self.id, 'source_ip': self.source_ip, 'attack_type': self.attack_type, 'risk_score': self.risk_score, 'severity': self.severity}
