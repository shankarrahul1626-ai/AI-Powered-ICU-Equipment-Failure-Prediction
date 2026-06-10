from utils.ui_components import *

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ICU Digital Twin",
    page_icon="🏥",
    layout="wide"
)

load_theme()
render_global_hud(
    title="ICU Digital Twin",
    chips=[
        "🏥 Real-Time ICU View",
        "📊 Equipment Status",
        "🧠 Digital Twin Analytics"
    ]
)

st.title("🏥 ICU Digital Twin")

st.markdown(
    "Real-Time ICU Equipment Visualization"
)

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(
    "data/features/risk_intelligence_data.csv"
)

# =====================================
# FILTERS
# =====================================

st.markdown("### Filter Selection")

hospital_options = sorted(df["hospital_name"].unique())
default_hospital = "CityCare Multi-Speciality Hospital"
if default_hospital not in hospital_options:
    default_hospital = hospital_options[0]

hospital_idx = hospital_options.index(default_hospital)

hospital = st.selectbox(
    "Hospital",
    hospital_options,
    index=hospital_idx
)

filtered = df[
    df["hospital_name"] == hospital
]

icu_options = sorted(filtered["icu_unit"].unique())
default_icu = "Neuro ICU"
if default_icu not in icu_options:
    default_icu = icu_options[0]

icu_idx = icu_options.index(default_icu)

icu = st.selectbox(
    "ICU Unit",
    icu_options,
    index=icu_idx
)

filtered = filtered[
    filtered["icu_unit"] == icu
]

# =====================================
# ICU OVERVIEW
# =====================================

st.subheader("📊 ICU Overview")

kpi_devices = len(filtered)
critical_assets = len(filtered[filtered["failure_risk_level"] == "Critical"])
high_assets = len(filtered[filtered["failure_risk_level"] == "High"])
moderate_assets = len(filtered[filtered["failure_risk_level"] == "Moderate"])
kpi_technicians = filtered["technician_assigned"].nunique()
kpi_rooms = filtered["room_number"].nunique()

risk_score = 100 - round(
    (critical_assets * 0.75 + high_assets * 0.45 + moderate_assets * 0.20)
    / max(kpi_devices, 1) * 100
)
risk_score = max(0, min(risk_score, 100))

card_html = """<div class='kpi-card {color}' style='border-color:{border};'>
    <div class='kpi-value'>{value}</div>
    <div class='kpi-label'>{label}</div>
</div>"""

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        card_html.format(
            value=kpi_devices,
            label="🖥 Devices",
            border="#38bdf8",
            color="blue"
        ),
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        card_html.format(
            value=critical_assets,
            label="⚠️ Critical Assets",
            border="#f87171",
            color="red"
        ),
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        card_html.format(
            value=kpi_technicians,
            label="👷 Technicians",
            border="#34d399",
            color="green"
        ),
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        card_html.format(
            value=kpi_rooms,
            label="🛌 Rooms",
            border="#fbbf24",
            color="yellow"
        ),
        unsafe_allow_html=True
    )

with c5:
    st.markdown(
        card_html.format(
            value=f"{risk_score}%",
            label="📉 Risk Score",
            border="#8b5cf6",
            color="purple"
        ),
        unsafe_allow_html=True
    )

st.divider()

# =====================================
# DIGITAL TWIN GRID
# =====================================

st.subheader("🛏 ICU Bed Layout")

rooms = filtered.sort_values(
    by="room_number"
)

for room in rooms["room_number"].unique():

    st.markdown(
        f"### Room {room}"
    )

    room_df = rooms[
        rooms["room_number"] == room
    ]

    cols = st.columns(4)

    for idx, (_, row) in enumerate(
        room_df.iterrows()
    ):

        with cols[idx % 4]:

            if row["failure_risk_level"] == "Critical":
                st.error(
                    f"""
Bed {row['bed_number']}

{row['equipment_type']}

🔴 Critical
"""
                )

            elif row["failure_risk_level"] == "High":
                st.warning(
                    f"""
Bed {row['bed_number']}

{row['equipment_type']}

🟠 High Risk
"""
                )

            else:
                st.success(
                    f"""
Bed {row['bed_number']}

{row['equipment_type']}

🟢 Healthy
"""
                )

st.divider()

# =====================================
# LIVE ASSET TABLE
# =====================================

st.subheader("📋 Asset Registry")

st.dataframe(
    filtered[
        [
            "equipment_id",
            "equipment_type",
            "room_number",
            "bed_number",
            "technician_assigned",
            "failure_risk_level",
            "maintenance_priority"
        ]
    ],
    width='stretch'
)

st.divider()

# =====================================
# CRITICAL ALERTS
# =====================================

st.subheader("🚨 Active Alerts")

critical = filtered[
    filtered["failure_risk_level"]
    == "Critical"
]

if len(critical) > 0:

    for _, row in critical.head(5).iterrows():

        st.error(
            f"""
Equipment ID: {row['equipment_id']}

Equipment: {row['equipment_type']}

Room: {row['room_number']}

Bed: {row['bed_number']}

Technician:
{row['technician_assigned']}

Recommendation:
{row['ai_recommendation']}
"""
        )

else:

    st.success(
        "No Critical Alerts"
    )
    c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "Ventilator Health",
        "92%"
    )

with c2:
    st.metric(
        "Infusion Pump",
        "89%"
    )

with c3:
    st.metric(
        "Patient Monitor",
        "95%"
    )

with c4:
    st.metric(
        "Defibrillator",
        "87%"
    )
    st.divider()

st.subheader(
    "📈 Live Equipment Telemetry"
)

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=[1,2,3,4,5,6],
        y=[20,40,35,60,55,75],
        mode="lines+markers",
        name="Ventilator"
    )
)

st.plotly_chart(
    fig,
    width='stretch'
)
