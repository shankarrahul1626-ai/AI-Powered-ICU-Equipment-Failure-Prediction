from utils.ui_components import *

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Business Intelligence",
    page_icon="💰",
    layout="wide"
)

load_theme()
render_global_hud(
    title="Business Intelligence",
    chips=[
        "💸 Financial Analytics",
        "📈 Executive KPIs",
        "🏥 Asset ROI Insights"
    ]
)
import streamlit as st
import pandas as pd

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Business Intelligence",
    page_icon="💰",
    layout="wide"
)

st.title("💰 MedGuard AI Business Intelligence Center")

st.markdown(
    "Executive Analytics for Hospital Asset Management"
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

st.subheader("📊 Executive KPIs")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Total Assets",
        f"{len(df):,}"
    )

with k2:
    st.metric(
        "Maintenance Cost",
        f"₹ {df['maintenance_cost'].sum():,.0f}"
    )

with k3:
    st.metric(
        "Downtime Hours",
        f"{df['downtime_hours'].sum():,.0f}"
    )

with k4:
    st.metric(
        "Avg Health Score",
        f"{df['health_score'].mean():.2f}"
    )

st.divider()

# =====================================
# COST ANALYTICS
# =====================================

st.subheader("💸 Maintenance Cost by Equipment Type")

cost_by_equipment = (
    df.groupby("equipment_type")[
        "maintenance_cost"
    ]
    .sum()
    .sort_values(
        ascending=False
    )
)

st.bar_chart(cost_by_equipment)

st.divider()

# =====================================
# DOWNTIME ANALYTICS
# =====================================

st.subheader("⏳ Downtime Analysis")

downtime = (
    df.groupby("equipment_type")[
        "downtime_hours"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)

st.bar_chart(downtime)

st.divider()

# =====================================
# MANUFACTURER PERFORMANCE
# =====================================

st.subheader("🏭 Manufacturer Performance")

manufacturer_health = (
    df.groupby("manufacturer")[
        "health_score"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)

st.bar_chart(manufacturer_health)

st.divider()

# =====================================
# TECHNICIAN PERFORMANCE
# =====================================

st.subheader("👨‍🔧 Technician Performance")

tech = (
    df.groupby(
        "technician_assigned"
    )
    .agg({
        "maintenance_cost": "sum",
        "equipment_id": "count"
    })
)

tech.columns = [
    "Total Maintenance Cost",
    "Assets Managed"
]

st.dataframe(
    tech,
    width='stretch'
)

st.divider()

# =====================================
# EQUIPMENT LIFECYCLE
# =====================================

st.subheader("🔄 Equipment Lifecycle Analysis")

lifecycle = (
    df[
        "equipment_lifecycle_stage"
    ]
    .value_counts()
)

st.bar_chart(lifecycle)

st.divider()

# =====================================
# RISK DISTRIBUTION
# =====================================

st.subheader("🚨 Risk Distribution")

risk_distribution = (
    df[
        "failure_risk_level"
    ]
    .value_counts()
)

st.bar_chart(risk_distribution)

st.divider()

# =====================================
# TOP CRITICAL ASSETS
# =====================================

st.subheader("🚨 Top Critical Assets")

critical_assets = df[

    df["failure_risk_level"]
    ==
    "Critical"

].sort_values(
    by="risk_score",
    ascending=False
)

st.dataframe(
    critical_assets[
        [
            "equipment_id",
            "equipment_type",
            "hospital_name",
            "risk_score",
            "maintenance_status"
        ]
    ].head(20),
    width='stretch'
)

st.divider()

# =====================================
# AI FINANCIAL SUMMARY
# =====================================

critical_count = len(
    df[
        df["failure_risk_level"]
        ==
        "Critical"
    ]
)

st.subheader("🤖 AI Executive Summary")

st.success(f"""
Total Assets Analyzed:
{len(df):,}

Total Maintenance Cost:
₹ {df['maintenance_cost'].sum():,.0f}

Total Downtime Hours:
{df['downtime_hours'].sum():,.0f}

Average Health Score:
{df['health_score'].mean():.2f}

Critical Assets:
{critical_count}

Recommendation:

Prioritize maintenance for critical ICU equipment.
Replace aging devices with consistently high downtime.
Focus on preventive maintenance to reduce operational costs.
""")
