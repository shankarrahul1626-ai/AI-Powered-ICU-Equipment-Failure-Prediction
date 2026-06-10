from utils.ui_components import *

import streamlit as st
import time

st.set_page_config(
    page_title="Live Prediction",
    page_icon="🤖",
    layout="wide"
)

load_theme()
render_global_hud(
    title="Live Prediction",
    chips=[
        "🚀 Instant Equipment Forecasts",
        "📊 Live Risk Scoring",
        "⚡ Rapid Failure Alerts"
    ]
)

from utils.model_loader import (
    rf_model,
    xgb_model,
    rul_model
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Live Prediction",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Live ICU Equipment Prediction Engine")

st.markdown("""
Predict equipment failures before they happen using:

✅ Random Forest AI

✅ XGBoost AI

✅ Remaining Useful Life Prediction

✅ Intelligent Risk Assessment
""")

st.divider()

# ==========================================
# INPUT FORM
# ==========================================

st.subheader("🏥 Equipment Parameters")

c1, c2, c3 = st.columns(3)

with c1:

    temperature = st.number_input(
        "Temperature",
        value=60.0
    )

    vibration = st.number_input(
        "Vibration",
        value=2.0
    )

    pressure = st.number_input(
        "Pressure",
        value=100.0
    )

    cpu_usage = st.number_input(
        "CPU Usage",
        value=50
    )

    battery_health = st.number_input(
        "Battery Health",
        value=90
    )

with c2:

    error_count = st.number_input(
        "Error Count",
        value=2
    )

    usage_hours = st.number_input(
        "Usage Hours",
        value=5000
    )

    equipment_age = st.number_input(
        "Equipment Age (Years)",
        value=5
    )

    days_since_maintenance = st.number_input(
        "Days Since Maintenance",
        value=60
    )

with c3:

    maintenance_cost = st.number_input(
        "Maintenance Cost",
        value=10000
    )

    downtime_hours = st.number_input(
        "Downtime Hours",
        value=5
    )

    criticality_score = st.number_input(
        "Criticality Score",
        value=60
    )

st.divider()

# ==========================================
# PREDICTION BUTTON
# ==========================================

if st.button("🚀 Run AI Prediction"):

    # ======================================
    # FEATURE ENGINEERING
    # ======================================

    health_score = (
        100
        - (temperature * 0.3)
        - (error_count * 2)
    )

    risk_score = (
        temperature * 0.4
        +
        vibration * 0.3
        +
        error_count * 0.3
    )

    maintenance_overdue_flag = (
        1 if days_since_maintenance > 120
        else 0
    )

    high_risk_flag = (
        1 if risk_score > 40
        else 0
    )

    critical_equipment_flag = (
        1 if criticality_score > 80
        else 0
    )

    # ======================================
    # LIVE AI STATUS
    # ======================================

    with st.status(
        "Running AI Analysis...",
        expanded=True
    ) as status:

        st.write(
            "Loading Random Forest Model..."
        )
        time.sleep(0.5)

        st.write(
            "Loading XGBoost Model..."
        )
        time.sleep(0.5)

        st.write(
            "Calculating Failure Probability..."
        )
        time.sleep(0.5)

        st.write(
            "Estimating Remaining Useful Life..."
        )
        time.sleep(0.5)

        status.update(
            label="Analysis Complete",
            state="complete"
        )

    # ======================================
    # PROGRESS BAR
    # ======================================

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    # ======================================
    # RANDOM FOREST FEATURES
    # ======================================

    features = [[

        temperature,
        vibration,
        pressure,
        cpu_usage,
        battery_health,
        error_count,
        usage_hours,
        equipment_age,
        days_since_maintenance,
        maintenance_cost,
        downtime_hours,
        criticality_score,
        health_score,
        risk_score,
        maintenance_overdue_flag,
        high_risk_flag,
        critical_equipment_flag

    ]]

    # ======================================
    # RANDOM FOREST PREDICTION
    # ======================================

    rf_prediction = rf_model.predict(
        features
    )[0]

    rf_probability = rf_model.predict_proba(
        features
    )[0][1]

    # ======================================
    # XGBOOST PREDICTION
    # ======================================

    xgb_prediction = xgb_model.predict(
        features
    )[0]

    # ======================================
# RUL PREDICTION
# ======================================

    rul_prediction = rul_model.predict(
        features
    )[0]
    # ======================================
    # RISK ENGINE
    # ======================================

    if rf_probability >= 0.90:

        risk_level = "CRITICAL"

    elif rf_probability >= 0.70:

        risk_level = "HIGH"

    elif rf_probability >= 0.40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    # ======================================
    # AI RECOMMENDATION
    # ======================================

    if risk_level == "CRITICAL":

        recommendation = (
            "Immediate Maintenance Required"
        )

    elif risk_level == "HIGH":

        recommendation = (
            "Schedule Technician Inspection"
        )

    elif risk_level == "MEDIUM":

        recommendation = (
            "Monitor Equipment Closely"
        )

    else:

        recommendation = (
            "Equipment Operating Normally"
        )

    # ======================================
    # RESULTS
    # ======================================

    st.divider()

    st.markdown("""
<div class='glass-card'>
<h2>🤖 AI Decision Engine</h2>
</div>
""", unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric(
            "Failure Probability",
            f"{rf_probability * 100:.2f}%"
    )

    with r2:
        st.metric(
            "Risk Level",
            risk_level
    )

    with r3:
        st.metric(
            "Predicted RUL",
            f"{rul_prediction:.0f} hrs"
    )
    st.divider()

    # ======================================
    # RECOMMENDATION PANEL
    # ======================================

    st.subheader(
        "🧠 AI Recommendation"
    )

    if risk_level == "CRITICAL":

        st.error(f"""
🚨 CRITICAL ALERT

Failure Probability:
{rf_probability*100:.2f}%

Recommended Action:

{recommendation}
""")

    elif risk_level == "HIGH":

        st.warning(
            recommendation
        )

    else:

        st.success(
            recommendation
        )

    # ======================================
    # TOAST ALERTS
    # ======================================

    st.toast(
        "AI Analysis Completed",
        icon="🤖"
    )

    if rf_probability > 0.90:

        st.toast(
            "Critical Equipment Detected",
            icon="🚨"
        )

    # ======================================
    # HEALTH VISUALIZATION
    # ======================================

    st.divider()

    st.subheader(
        "📈 Equipment Health Indicators"
    )

    h1, h2 = st.columns(2)

    with h1:

        st.write("Health Score")

        st.progress(
            min(
                max(
                    int(health_score),
                    0
                ),
                100
            )
        )

        st.write(
            f"{health_score:.2f}/100"
        )

    with h2:

        st.write("Risk Score")

        risk_progress = min(
            int(risk_score),
            100
        )

        st.progress(
            risk_progress
        )

        st.write(
            f"{risk_score:.2f}/100"
        )
