from utils.ui_components import *

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Command Center",
    page_icon="🏥",
    layout="wide"
)

load_theme()
render_global_hud(
    title="Command Center",
    chips=[
        "🌍 Central Operations Hub",
        "🧠 Strategic Intelligence",
        "🚨 Alert Management"
    ]
)

st.markdown("""
<div class='glass-card'>
<h1>🌍 Global Hospital Command Center</h1>
</div>
""", unsafe_allow_html=True)

k1,k2,k3,k4,k5,k6 = st.columns(6)

k1.metric("Hospitals",12)

k2.metric("Devices",10000)

k3.metric("Critical Alerts",14)

k4.metric("Technicians",43)

k5.metric("Uptime","99.8%")

k6.metric("Savings","₹1.2 Cr")
st.markdown(
    "Enterprise Healthcare Operations Dashboard"
)

# ==============================
# KPI SECTION
# ==============================

k1,k2,k3,k4,k5,k6 = st.columns(6)

k1.metric(
    "Equipment",
    "10,000"
)

k2.metric(
    "Hospitals",
    "12"
)

k3.metric(
    "Critical Alerts",
    "8"
)

k4.metric(
    "Fleet Health",
    "94%"
)

k5.metric(
    "AI Accuracy",
    "99.95%"
)

k6.metric(
    "Technicians",
    "24 Online"
)

st.divider()

# ==============================
# ALERTS
# ==============================

st.subheader("🚨 Active Alerts")

c1,c2,c3 = st.columns(3)

with c1:
    st.error("""
Ventilator VNT-2045

Failure Risk: 96%
""")

with c2:
    st.error("""
Defibrillator DEF-1120

Failure Risk: 93%
""")

with c3:
    st.warning("""
Monitor MON-5512

Failure Risk: 81%
""")

st.divider()

# ==============================
# HOSPITAL TABLE
# ==============================

st.subheader("🏥 Hospital Network")

hospital_df = pd.DataFrame({

    "Hospital":[
        "Apollo",
        "Fortis",
        "Manipal",
        "Narayana",
        "Aster"
    ],

    "ICU Units":[
        12,
        9,
        8,
        15,
        6
    ],

    "Equipment":[
        2140,
        1830,
        1520,
        2800,
        1110
    ]
})

st.dataframe(
    hospital_df,
    width='stretch'
)

st.divider()

# ==============================
# HEALTH DISTRIBUTION
# ==============================

st.subheader("📊 Equipment Health")

health_data = pd.DataFrame({
    "Status":[
        "Healthy",
        "Warning",
        "Critical",
        "Maintenance Due"
    ],
    "Count":[
        8200,
        1200,
        200,
        400
    ]
})

st.bar_chart(
    health_data.set_index("Status")
)

st.divider()

# ==============================
# TECHNICIANS
# ==============================

st.subheader("🔧 Technician Operations")

tech_df = pd.DataFrame({

    "Technician":[
        "John",
        "Sarah",
        "Rahul",
        "Anita"
    ],

    "Status":[
        "On Duty",
        "Maintenance",
        "Available",
        "Emergency Call"
    ]
})

st.dataframe(
    tech_df,
    width='stretch'
)

st.divider()

# ==============================
# AI SUMMARY
# ==============================

st.subheader("🤖 AI Executive Summary")

st.success("""
10,000 devices analyzed.

94% operating normally.

127 devices require maintenance.

8 devices classified as critical.

Recommended Action:

Deploy technicians to ICU Unit 4.
""")
if st.button("🚨 Emergency Mode"):

    st.error("""
    CRITICAL INCIDENT DETECTED

    Ventilator Failure Probability: 97%

    Dispatch Technician Immediately
    """)

    st.balloons()
    import pandas as pd

map_data = pd.DataFrame({

    "lat":[
        12.9716,
        19.0760,
        13.0827,
        17.3850
    ],

    "lon":[
        77.5946,
        72.8777,
        80.2707,
        78.4867
    ]
})

st.map(map_data)
st.error("""
🚨 AI Situation Report

Critical Assets : 8

High Risk Assets : 127

Predicted Downtime : 14 Hours

Recommended Action :

Deploy Team Alpha
""")
import plotly.express as px

# Load data for analytics
df = pd.read_csv(
    "data/features/risk_intelligence_data.csv"
)

health_df = df.groupby(
    "equipment_type"
)["health_score"].mean().reset_index()

fig = px.treemap(
    health_df,
    path=["equipment_type"],
    values="health_score",
    color="health_score"
)

st.plotly_chart(fig, width='stretch')
import time

alerts = [

    "🚨 Ventilator VNT-104 predicted failure",
    "⚠ Infusion Pump maintenance due",
    "🔧 Technician assigned to ICU-B",
    "🟢 Defibrillator recovered"

]

placeholder = st.empty()

for alert in alerts:

    placeholder.warning(alert)
    time.sleep(1)
