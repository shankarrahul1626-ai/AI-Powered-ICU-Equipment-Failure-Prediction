from utils.ui_components import *
import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

st.set_page_config(
    page_title="Predictive Maintenance Workbench",
    page_icon="🔧",
    layout="wide"
)

load_theme()
render_global_hud(
    title="Predictive Maintenance Workbench",
    chips=[
        "🔧 Predictive Maintenance AI",
        "📅 Scheduled Interventions",
        "📊 Priority Risk Model"
    ]
)

st.title("🔧 Predictive Maintenance Workbench")

st.markdown("""
Analyze equipment health,
failure risk, maintenance priority,
and AI recommendations.
""")
df = pd.read_csv(
    "data/features/risk_intelligence_data.csv"
)
# =====================================
# LOAD AI MODELS
# =====================================

rf_model = joblib.load(
    "models/enterprise_random_forest.pkl"
)

rul_model = joblib.load(
    "models/rul_model.pkl"
)
equipment_id = st.selectbox(
    "Select Equipment",
    df["equipment_id"].unique()
)
selected = df[
    df["equipment_id"] == equipment_id
].iloc[0]
# =====================================
# RANDOM FOREST FEATURES (17)
# =====================================

rf_features = [[
    selected["temperature"],
    selected["vibration"],
    selected["pressure"],
    selected["cpu_usage"],
    selected["battery_health"],
    selected["error_count"],
    selected["usage_hours"],
    selected["equipment_age"],
    selected["days_since_maintenance"],
    selected["maintenance_cost"],
    selected["downtime_hours"],
    selected["criticality_score"],
    selected["health_score"],
    selected["risk_score"],
    selected["maintenance_overdue_flag"],
    selected["high_risk_flag"],
    selected["critical_equipment_flag"]
]]

# =====================================
# RUL FEATURES (10)
# =====================================

rul_features = [[
    selected["temperature"],
    selected["vibration"],
    selected["pressure"],
    selected["cpu_usage"],
    selected["battery_health"],
    selected["error_count"],
    selected["usage_hours"],
    selected["equipment_age"],
    selected["health_score"],
    selected["risk_score"]
]]

# =====================================
# FAILURE PREDICTION
# =====================================

failure_probability = (
    rf_model.predict_proba(rf_features)[0][1]
)

failure_percent = (
    failure_probability * 100
)
# =====================================
# RUL PREDICTION
# =====================================

rul_prediction = (
    rul_model.predict(rul_features)[0]
)
# =====================================
# RISK ENGINE
# =====================================

if failure_percent >= 90:
    live_risk = "CRITICAL"

elif failure_percent >= 70:
    live_risk = "HIGH"

elif failure_percent >= 40:
    live_risk = "MEDIUM"

else:
    live_risk = "LOW"

st.write(selected)
st.divider()

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Failure Probability",
        f"{failure_percent:.2f}%"
    )

with k2:
    st.metric(
        "Live Risk",
        live_risk
    )

with k3:
    st.metric(
        "Predicted RUL",
        f"{rul_prediction:.0f} hrs"
    )

with k4:
    st.metric(
        "Priority",
        selected["maintenance_priority"]
    )
    st.divider()
st.subheader("🏥 Asset Health")

st.progress(
    int(selected["health_score"])
)

st.write(
    f"{selected['health_score']:.1f}/100"
)

st.divider()
st.subheader("🏥 Equipment Profile")

profile_cols = [

    "equipment_type",
    "usage_hours",
    "equipment_age",
    "health_score",
    "risk_score"

]

available_cols = [
    c for c in profile_cols
    if c in df.columns
]

st.dataframe(
    selected[available_cols].to_frame(),
    width='stretch'
)
import plotly.graph_objects as go
st.divider()

st.subheader("🚨 Failure Risk Gauge")

risk_value = min(
    float(selected["risk_score"]),
    100
)

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=risk_value,
        title={
            "text": "Risk Score"
        },
        gauge={
            "axis": {
                "range": [0,100]
            }
        }
    )
)

st.plotly_chart(
    fig,
    width='stretch'
)
st.divider()

st.subheader("🧠 AI Recommendation")

if live_risk == "CRITICAL":

    st.error("""
🚨 Immediate Maintenance Required

Failure risk extremely high.

Dispatch technician immediately.
""")

elif live_risk == "HIGH":

    st.warning("""
⚠ Technician Inspection Recommended

Schedule maintenance within 24 hours.
""")

else:

    st.success("""
✅ Equipment Operating Normally
""")
st.divider()

st.subheader(
    "💰 Maintenance Delay Simulator"
)

delay_days = st.slider(
    "Delay Maintenance",
    0,
    30,
    5
)

estimated_cost = delay_days * 15000

st.metric(
    "Estimated Additional Cost",
    f"₹{estimated_cost:,}"
)
