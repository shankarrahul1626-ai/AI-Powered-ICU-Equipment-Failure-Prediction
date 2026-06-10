from utils.ui_components import *

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Maintenance Hub",
    page_icon="🔧",
    layout="wide"
)

load_theme()
render_global_hud(
    title="Maintenance Hub",
    chips=[
        "🔧 Maintenance Operations",
        "📋 Work Order Coordination",
        "🛠️ Technician Dispatch"
    ]
)

st.title("🔧 Maintenance Hub")

st.markdown(
    "Hospital Maintenance Operations Center"
)

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(
    "data/features/risk_intelligence_data.csv"
)

# =====================================
# KPI SECTION
# =====================================

total_assets = len(df)

maintenance_due = len(
    df[df["maintenance_status"] == "Maintenance Due"]
)

critical_assets = len(
    df[df["failure_risk_level"] == "Critical"]
)

avg_cost = round(
    df["maintenance_cost"].mean(),
    2
)

k1,k2,k3,k4 = st.columns(4)

with k1:
    st.metric(
        "Total Assets",
        total_assets
    )

with k2:
    st.metric(
        "Maintenance Due",
        maintenance_due
    )

with k3:
    st.metric(
        "Critical Assets",
        critical_assets
    )

with k4:
    st.metric(
        "Avg Cost (₹)",
        avg_cost
    )

st.divider()

# =====================================
# WORK ORDER CENTER
# =====================================

st.subheader("📋 Open Work Orders")

work_orders = df[
    df["maintenance_status"] == "Maintenance Due"
]

st.dataframe(
    work_orders[
        [
            "equipment_id",
            "equipment_type",
            "hospital_name",
            "technician_assigned",
            "maintenance_priority",
            "ai_recommendation"
        ]
    ],
    width='stretch'
)

st.divider()

# =====================================
# TECHNICIAN LOAD
# =====================================

st.subheader("👨‍🔧 Technician Workload")

tech_load = (
    df.groupby(
        "technician_assigned"
    )
    .size()
    .reset_index(name="Assets")
)

fig = px.bar(
    tech_load,
    x="technician_assigned",
    y="Assets",
    title="Assets Assigned per Technician"
)

st.plotly_chart(
    fig,
    width='stretch'
)

st.divider()

# =====================================
# MAINTENANCE COST
# =====================================

st.subheader("💰 Maintenance Cost Analysis")

cost_df = (
    df.groupby(
        "equipment_type"
    )["maintenance_cost"]
    .mean()
    .reset_index()
)

fig = px.bar(
    cost_df,
    x="equipment_type",
    y="maintenance_cost",
    title="Average Maintenance Cost"
)

st.plotly_chart(
    fig,
    width='stretch'
)

st.divider()

# =====================================
# DOWNTIME ANALYTICS
# =====================================

st.subheader("⏱ Downtime Analysis")

downtime_df = (
    df.groupby(
        "equipment_type"
    )["downtime_hours"]
    .mean()
    .reset_index()
)

fig = px.pie(
    downtime_df,
    names="equipment_type",
    values="downtime_hours",
    hole=0.5,
    title="Downtime Distribution"
)

st.plotly_chart(
    fig,
    width='stretch'
)

st.divider()

# =====================================
# SERVICE SCHEDULE
# =====================================

st.subheader("📅 Service Schedule")

schedule = df[
    [
        "equipment_id",
        "equipment_type",
        "technician_assigned",
        "maintenance_status"
    ]
].head(20)

st.dataframe(
    schedule,
    width='stretch'
)

st.divider()

# =====================================
# AI ACTION CENTER
# =====================================

st.subheader("🤖 AI Maintenance Actions")

critical = df[
    df["failure_risk_level"] == "Critical"
]

for _, row in critical.head(5).iterrows():

    st.error(
        f"""
Equipment ID: {row['equipment_id']}

Equipment Type: {row['equipment_type']}

Priority: {row['maintenance_priority']}

Technician: {row['technician_assigned']}

Recommendation:
{row['ai_recommendation']}
"""
    )
