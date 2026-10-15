# NEXUS Team Guide

## Quick Start

### Clone Repository
```bash
git clone https://github.com/vnvsvv/Nexus-Project.git
cd Nexus-Project
```

### Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Components

**1. Generate Data:**
```bash
python3 scripts/generate_data.py
```

**2. Train Models:**
```bash
python3 src/models/network_ids.py
python3 src/models/log_anomaly_detector.py
```

**3. View Dashboard:**
```bash
streamlit run src/dashboard/app.py
```

## Project Structure

- **src/models/**: Machine learning models
- **src/features/**: Data loading & preprocessing
- **src/correlation/**: Alert correlation & risk scoring
- **src/dashboard/**: Streamlit UI
- **src/utils/**: Helper functions
- **config/**: Configuration files
- **data/**: Datasets
- **scripts/**: Training scripts
- **docs/**: Documentation
- **tests/**: Unit tests

## Team Roles

| Member | Responsibility |
|--------|-----------------|
| Anas | ML Models, Architecture |
| Omar | Data Engineering, Dataset prep |
| Rakan | Security, Correlation Engine |
| Bashar | Dashboard, Frontend |

## Git Workflow

```bash
# Update code
git pull origin main

# Make changes
git add .
git commit -m "Description"

# Push changes
git push origin main
```

## Key Metrics

- Network IDS Accuracy: **85%**
- Anomaly Detection: **Trained**
- Dashboard: **Live**

## Next Phase

- Real-time data ingestion
- Threat Intelligence APIs
- Automated response
- Database integration

---
Last Updated: October 15, 2026
