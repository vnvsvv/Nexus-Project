import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.config import config

st.set_page_config(page_title="NEXUS Dashboard", layout="wide")

st.title("NEXUS Security Monitoring Platform")
st.markdown("AI-Powered Threat Detection & Incident Response")

# Sidebar
st.sidebar.header("Configuration")
company = config.get_company_name()
network = config.get_network_cidr()

st.sidebar.write(f"Company: {company}")
st.sidebar.write(f"Network: {network}")

# Main Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Alerts", "1,245", "+12%")

with col2:
    st.metric("High Risk", "45", "+3")

with col3:
    st.metric("System Status", "Active", "OK")

st.divider()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Detection Breakdown")
    data = {'Type': ['Network', 'Logs', 'Correlation'], 'Count': [450, 320, 475]}
    df = pd.DataFrame(data)
    st.bar_chart(df.set_index('Type'))

with col2:
    st.subheader("Risk Distribution")
    data = {'Severity': ['Critical', 'High', 'Medium', 'Low'], 'Count': [15, 45, 120, 200]}
    df = pd.DataFrame(data)
    st.bar_chart(df.set_index('Severity'))

st.divider()

# Alerts Table
st.subheader("Recent Alerts")
alert_data = {
    'Timestamp': pd.date_range('2026-10-15', periods=5, freq='H'),
    'Source IP': ['192.168.1.50', '192.168.1.75', '192.168.1.30', '192.168.1.100', '192.168.1.45'],
    'Alert Type': ['Brute Force', 'Anomaly', 'Port Scan', 'Malware', 'Data Exfil'],
    'Risk Score': [0.95, 0.72, 0.58, 0.88, 0.65],
    'Status': ['Critical', 'High', 'Medium', 'Critical', 'High']
}
df_alerts = pd.DataFrame(alert_data)
st.dataframe(df_alerts, use_container_width=True)

st.divider()
st.write("NEXUS v1.0 | Philadelphia University Capstone Project")
