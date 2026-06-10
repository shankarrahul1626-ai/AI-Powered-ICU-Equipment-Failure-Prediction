from utils.ui_components import *

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

load_theme()
render_global_hud(
    title="Executive Dashboard",
    chips=[
        "📊 Executive Analytics",
        "🌐 Live ICU Monitoring",
        "🧠 AI Operational Mode"
    ]
)

st.title("📊 Executive Dashboard")

st.markdown(
    "Hospital Asset Intelligence & Financial Analytics"
)

# ==========================================
# KPI SECTION
# ==========================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Annual Savings",
        "₹1.2 Cr",
        "+18%"
    )

with k2:
    st.metric(
        "Downtime Reduction",
        "31%",
        "+6%"
    )

with k3:
    st.metric(
        "Maintenance Efficiency",
        "87%",
        "+12%"
    )

with k4:
    st.metric(
        "Failure Prevention",
        "94%",
        "+4%"
    )
st.divider()
import time

st.markdown("## 🟢 Live ICU Monitoring")

status = st.empty()

for i in range(3):
    status.success(
        f"Monitoring Cycle {i+1} Complete"
    )
    time.sleep(0.5)

st.success(
    "10,000+ ICU devices currently connected and monitored."
)
import plotly.express as px
import pandas as pd

health_df = pd.DataFrame({
    "Status":[
        "Healthy",
        "Warning",
        "Critical"
    ],
    "Count":[
        8420,
        1180,
        400
    ]
})

fig = px.pie(
    health_df,
    values="Count",
    names="Status",
    hole=0.65,
    title="Equipment Fleet Health"
)

st.plotly_chart(
    fig,
    width='stretch'
)
st.markdown("""
<div style="
background:linear-gradient(
90deg,
#1e3a8a,
#2563eb
);
padding:25px;
border-radius:20px;
color:white;
">

<h2>🧠 AI Executive Summary</h2>

<ul>
<li>24% reduction in failure incidents</li>
<li>31% reduction in downtime</li>
<li>₹1.2 Crore projected savings</li>
<li>94% failure prevention accuracy</li>
<li>Ventilator fleet requires attention</li>
</ul>

</div>
""", unsafe_allow_html=True)
st.warning(
    "⚠ 3 Critical Assets Require Immediate Inspection"
)
# ==========================================
# REAL-TIME MONITORING
# ==========================================

import time

st.subheader("🟢 Live ICU Monitoring")

with st.status(
    "Monitoring ICU Equipment Network...",
    expanded=True
) as status:

    st.write("🫁 Checking Ventilator Fleet...")
    time.sleep(0.5)

    st.write("💉 Checking Infusion Pumps...")
    time.sleep(0.5)

    st.write("📈 Checking Patient Monitors...")
    time.sleep(0.5)

    st.write("⚡ Checking Defibrillators...")
    time.sleep(0.5)

    st.write("🤖 Running AI Risk Analysis...")
    time.sleep(0.5)

    status.update(
        label="All Systems Operational",
        state="complete"
    )

st.success(
    "10,000+ ICU devices currently connected and monitored."
)

st.divider()
st.subheader("🏥 Fleet Status")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.success("🫁 Ventilators\n\nHealthy")

with c2:
    st.success("💉 Infusion Pumps\n\nHealthy")

with c3:
    st.warning("📈 Patient Monitors\n\n2 Warnings")

with c4:
    st.error("⚡ Defibrillators\n\n1 Critical Alert")
# ==========================================
# COST ANALYTICS
# ==========================================

st.subheader("💰 Maintenance Cost Analytics")

cost_data = pd.DataFrame({
    "Month":[
        "Jan","Feb","Mar",
        "Apr","May","Jun"
    ],
    "Cost":[
        420000,
        380000,
        350000,
        310000,
        280000,
        250000
    ]
})

fig = px.line(
    cost_data,
    x="Month",
    y="Cost",
    markers=True,
    title="Maintenance Cost Trend"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ==========================================
# HOSPITAL COMPARISON
# ==========================================

st.subheader("🏥 Hospital Comparison")

hospital_df = pd.DataFrame({
    "Hospital":[
        "Apollo",
        "Fortis",
        "Manipal",
        "Aster",
        "Narayana"
    ],
    "Asset Health":[
        92,
        89,
        94,
        90,
        88
    ]
})

fig = px.bar(
    hospital_df,
    x="Hospital",
    y="Asset Health",
    title="Hospital Asset Health Score"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ==========================================
# FAILURE FORECAST
# ==========================================

st.subheader("🚨 Predicted Failures")

forecast_df = pd.DataFrame({
    "Month":[
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ],
    "Predicted Failures":[
        35,
        32,
        28,
        24,
        21,
        18
    ]
})

fig = px.area(
    forecast_df,
    x="Month",
    y="Predicted Failures",
    title="Failure Forecast Trend"
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ==========================================
# EXECUTIVE INSIGHTS
# ==========================================

st.subheader("🧠 AI Executive Insights")

st.success("""
AI Analysis

• Failure rate reduced by 24%

• Maintenance efficiency improved by 17%

• Downtime reduced by 31%

• Projected annual savings:
₹1.2 Crore

• Highest risk asset:
Ventilator Fleet
""")
