from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.models import db, NetworkAlert, Incident
from src.utils.helpers import Logger
from src.correlation.alert_correlation import RiskScoringEngine

logger = Logger.setup()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nexus:nexus_secure_pass_2026@localhost/nexus_db'
db.init_app(app)
CORS(app)

model = joblib.load('src/models/advanced_network_ids.pkl')
scaler = joblib.load('src/models/advanced_network_ids_scaler.pkl')
risk_engine = RiskScoringEngine()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK'})

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        features = np.array([[float(data.get('src_port', 0)), float(data.get('dst_port', 0)), float(data.get('packet_length', 0)), float(data.get('packet_count', 0)), float(data.get('duration', 0)), float(data.get('protocol_encoded', 0))]])
        features_scaled = scaler.transform(features)
        prediction = int(model.predict(features_scaled)[0])
        confidence = float(model.predict_proba(features_scaled)[0].max())
        alert_type = str(model.classes_[prediction])
        
        alert = NetworkAlert(src_ip=data.get('src_ip'), dst_ip=data.get('dst_ip'), src_port=int(data.get('src_port', 0)), dst_port=int(data.get('dst_port', 0)), protocol=data.get('protocol'), alert_type=alert_type, confidence=confidence)
        db.session.add(alert)
        db.session.commit()
        
        return jsonify({'alert_id': alert.id, 'alert_type': alert_type, 'confidence': confidence, 'status': 'CREATED'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    alerts = NetworkAlert.query.all()
    return jsonify([a.to_dict() for a in alerts])

@app.route('/api/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([i.to_dict() for i in incidents])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({'total_alerts': NetworkAlert.query.count(), 'open_incidents': Incident.query.filter_by(status='OPEN').count()})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        logger.info("Database initialized!")
    app.run(host='0.0.0.0', port=5000, debug=True)
