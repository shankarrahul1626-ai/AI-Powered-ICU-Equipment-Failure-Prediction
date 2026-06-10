from utils.ui_components import *

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Copilot",
    page_icon="🤖",
    layout="wide"
)

load_theme()
render_global_hud(
    title="AI Copilot",
    chips=[
        "🤖 Conversational AI Assist",
        "📌 Smart Recommendations",
        "📈 Risk Query Engine"
    ]
)

st.title("🤖 MedGuard AI Copilot")

st.markdown(
    "Ask questions about ICU equipment, maintenance, and risk intelligence."
)

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(
    "data/features/risk_intelligence_data.csv"
)

# =====================================
# CHAT INPUT
# =====================================
question = st.chat_input(
    "Ask MedGuard AI..."
)

# =====================================
# QUERY ENGINE
# =====================================

if question:
    with st.chat_message("user"):
        st.write(question)

    q = question.lower()

    # Critical Assets

    if "critical" in q:

        result = df[
            df["failure_risk_level"]
            == "Critical"
        ]

        with st.chat_message("assistant"):

            st.write(
                "🚨 Here are the critical assets."
        )

            st.dataframe(
                result.head(20),
                width='stretch'
        )

    # Maintenance Due

    elif "maintenance" in q:

        result = df[
            df["maintenance_status"]
            == "Maintenance Due"
        ]

        with st.chat_message("assistant"):

            st.write(
                "🔧 Equipment requiring maintenance."
        )

            st.dataframe(
                result.head(20),
                width='stretch'
    )

    # Ventilator

    elif "ventilator" in q:

        result = df[
            df["equipment_type"]
            == "Ventilator"
        ]

        with st.chat_message("assistant"):

            st.write(
                "🫁 Ventilator fleet status."
        )

            st.dataframe(
                result.head(20),
                width='stretch'
    )

    # High Risk

    elif "risk" in q:

        result = df.sort_values(
            by="risk_score",
            ascending=False
        )

        with st.chat_message("assistant"):

            st.write(
                "⚠ Highest Risk Equipment"
            )

            st.dataframe(
                result.head(20),
                width='stretch'
        )

    # Technician

    elif "technician" in q:

        tech = (
            df.groupby(
                "technician_assigned"
            )
            .size()
            .reset_index(name="Assets")
        )

        with st.chat_message("assistant"):

            st.write(
                "👨‍🔧 Technician Workload"
            )

            st.dataframe(
                tech,
                width='stretch'
            )

    else:

        st.info(
            "Try asking about critical assets, ventilators, risk, maintenance, or technicians."
        )

# =====================================
# QUICK ACTIONS
# =====================================

st.divider()

st.subheader("⚡ Quick AI Actions")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button(
        "Show Critical Assets"
    ):
        critical = df[
            df["failure_risk_level"]
            == "Critical"
        ]

        st.dataframe(
            critical.head(20),
            width='stretch'
        )

with c2:
    if st.button(
        "Maintenance Due"
    ):
        due = df[
            df["maintenance_status"]
            == "Maintenance Due"
        ]

        st.dataframe(
            due.head(20),
            width='stretch'
        )

with c3:
    if st.button(
        "Highest Risk Devices"
    ):
        risk = df.sort_values(
            by="risk_score",
            ascending=False
        )

        st.dataframe(
            risk.head(20),
            width='stretch'
        )
