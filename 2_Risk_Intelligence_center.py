from utils.ui_components import *

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Risk Intelligence Center",
    page_icon="🚨",
    layout="wide"
)

load_theme()
render_global_hud(
    title="Risk Intelligence Center",
    chips=[
        "⚠️ Risk Intelligence Active",
        "🔍 Failure Probability Analysis",
        "📡 24/7 Surveillance"
    ]
)

st.title("🚨 Risk Intelligence Center")

st.markdown(
    "AI-Powered Equipment Risk Monitoring & Failure Intelligence"
)

# =====================================
# KPI SECTION
# =====================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Critical Assets",
        "127"
    )

with c2:
    st.metric(
        "High Risk Assets",
        "846"
    )

with c3:
    st.metric(
        "Medium Risk Assets",
        "2140"
    )

with c4:
    st.metric(
        "Healthy Assets",
        "6887"
    )

st.divider()

# =====================================
# FAILURE PROBABILITY TABLE
# =====================================

st.subheader("🔥 Top Failure Risks")

risk_df = pd.DataFrame({
    "Equipment ID":[
        "VNT-2045",
        "MON-3021",
        "INF-1190",
        "DEF-7721",
        "ECG-8840"
    ],
    "Equipment":[
        "Ventilator",
        "Patient Monitor",
        "Infusion Pump",
        "Defibrillator",
        "ECG Machine"
    ],
    "Failure Probability":[
        92,
        88,
        83,
        79,
        74
    ],
    "Recommendation":[
        "Immediate Inspection",
        "Replace Sensor",
        "Maintenance Required",
        "Battery Check",
        "Inspection Due"
    ]
})

st.dataframe(
    risk_df,
    width='stretch'
)

st.divider()

# =====================================
# RISK DISTRIBUTION
# =====================================

st.subheader("📊 Risk Distribution")

risk_data = pd.DataFrame({
    "Category":[
        "Critical",
        "High",
        "Medium",
        "Low"
    ],
    "Count":[
        127,
        846,
        2140,
        6887
    ]
})

fig = px.pie(
    risk_data,
    names="Category",
    values="Count",
    hole=0.5,
    title="Equipment Risk Distribution"
)

st.plotly_chart(
    fig,
    width='stretch'
)

st.divider()

# =====================================
# RISK HEATMAP DATA
# =====================================

st.subheader("🌡 ICU Risk Heatmap")

heatmap_df = pd.DataFrame({
    "ICU Unit":[
        "ICU-A",
        "ICU-B",
        "ICU-C",
        "ICU-D",
        "ICU-E"
    ],
    "Risk Score":[
        85,
        63,
        42,
        77,
        55
    ]
})

fig = px.bar(
    heatmap_df,
    x="ICU Unit",
    y="Risk Score",
    title="Risk Score by ICU Unit"
)

st.plotly_chart(
    fig,
    width='stretch'
)

st.divider()

# =====================================
# AI RECOMMENDATIONS
# =====================================

st.subheader("🤖 AI Recommendations")

risk_df = pd.read_csv(
    "data/features/risk_intelligence_data.csv"
)

critical_assets = risk_df[
    risk_df["failure_risk_level"] == "Critical"
].head(10)

if len(critical_assets) > 0:

    for _, row in critical_assets.iterrows():

        st.error(
            f"""
Equipment ID: {row['equipment_id']}

Risk Level: {row['failure_risk_level']}

Maintenance Priority:
{row['maintenance_priority']}

Recommendation:
{row['ai_recommendation']}
"""
        )

else:

    st.success(
        "No critical assets detected."
    )
st.divider()

st.subheader("🔍 Risk Explorer")

risk_filter = st.selectbox(
    "Select Risk Level",
    [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]
)

filtered_df = risk_df[
    risk_df["failure_risk_level"] == risk_filter
]

st.dataframe(
    filtered_df[
        [
            "equipment_id",
            "failure_risk_level",
            "maintenance_priority",
            "downtime_cost_impact",
            "ai_recommendation"
        ]
    ],
    width='stretch'
)
risk_df = pd.read_csv(
    "data/features/risk_intelligence_data.csv"
)

critical_count = len(
    risk_df[
        risk_df["failure_risk_level"] == "Critical"
    ]
)

high_count = len(
    risk_df[
        risk_df["failure_risk_level"] == "High"
    ]
)

medium_count = len(
    risk_df[
        risk_df["failure_risk_level"] == "Medium"
    ]
)

low_count = len(
    risk_df[
        risk_df["failure_risk_level"] == "Low"
    ]
)
c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "Critical Assets",
        critical_count
    )

with c2:
    st.metric(
        "High Risk Assets",
        high_count
    )

with c3:
    st.metric(
        "Medium Risk Assets",
        medium_count
    )

with c4:
    st.metric(
        "Low Risk Assets",
        low_count
    )
