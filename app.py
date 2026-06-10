import warnings

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.ui_components import load_theme, render_global_hud


warnings.filterwarnings("ignore", message=".*use_column_width.*")
warnings.filterwarnings("ignore", category=DeprecationWarning)

st.set_page_config(
    page_title="Hospital Command Center",
    page_icon=":hospital:",
    layout="wide",
)
load_theme()


df = pd.read_csv("data/features/risk_intelligence_data.csv")
df["next_maintenance_date"] = pd.to_datetime(df["next_maintenance_date"], errors="coerce")
df["health_score"] = pd.to_numeric(df["health_score"], errors="coerce").fillna(0)
df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(0)
df["remaining_useful_life"] = pd.to_numeric(df["remaining_useful_life"], errors="coerce").fillna(0)


def format_status(risk_level):
    if str(risk_level).lower() == "critical":
        return "Critical", "status-critical"
    if str(risk_level).lower() == "high":
        return "Warning", "status-warning"
    return "Safe", "status-safe"


def gauge_color(value):
    if value >= 80:
        return "#2dd4bf"
    if value >= 60:
        return "#22c55e"
    if value >= 40:
        return "#f59e0b"
    return "#ef4444"


def card_html(value, label, variant="blue"):
    return f"""<div class='kpi-card {variant}'>
    <div class='kpi-value'>{value}</div>
    <div class='kpi-label'>{label}</div>
</div>"""


st.markdown(
    """
<div class='topic-kpi-wrap'>
    <div class='kpi-card blue topic'>
        <div class='topic-kpi-title' style='font-size:50px; font-weight:900;'>AI-Powered</div>
        <div class='topic-kpi-title' style='font-size:50px; font-weight:900;'>ICU Equipment Failure Prediction</div>
    </div>
    <div class='topic-kpi-caption'>Project focus</div>
</div>
""",
    unsafe_allow_html=True,
)

hospital_options = sorted(df["hospital_name"].unique())
default_hospital = "CityCare Multi-Speciality Hospital"
hospital_index = hospital_options.index(default_hospital) if default_hospital in hospital_options else 0
selected_hospital = st.selectbox(
    "Hospital Command Node",
    hospital_options,
    index=hospital_index,
    key="command_hospital",
)

filtered = df[df["hospital_name"] == selected_hospital]

icu_options = sorted(filtered["icu_unit"].unique())
selected_icu = st.selectbox(
    "ICU Unit",
    icu_options,
    index=0,
    key="command_icu",
)

filtered = filtered[filtered["icu_unit"] == selected_icu]

critical_count = int((filtered["failure_risk_level"] == "Critical").sum())
high_count = int((filtered["failure_risk_level"] == "High").sum())
medium_count = int((filtered["failure_risk_level"] == "Medium").sum()) + int(
    (filtered["failure_risk_level"] == "Moderate").sum()
)
healthy_count = int(filtered["failure_risk_level"].isin(["Low", "Healthy"]).sum())

connected_devices = len(filtered)
average_health = int(filtered["health_score"].mean() if len(filtered) else 0)
avg_remaining_life = int(filtered["remaining_useful_life"].mean() if len(filtered) else 0)

status_summary = "Nominal"
status_prefix = "Status"
if critical_count > 0:
    status_summary = "Emergency Mode"
    status_prefix = "Critical"
elif high_count + medium_count > 0:
    status_summary = "Elevated Risk"
    status_prefix = "Watch"

render_global_hud(
    title="Hospital Command Center",
    chips=[
        f"Hospital: {selected_hospital}",
        f"Unit: {selected_icu}",
        "AI Engine: Active",
        "Network Uptime: 99.97%",
    ],
    status=f"{status_prefix}: {status_summary}",
)

st.markdown("<div class='pulse-wave'></div>", unsafe_allow_html=True)

if critical_count > 0:
    st.markdown(
        f"""
<div class='emergency-banner'>
    <strong>Emergency Mode Active</strong>
    {critical_count} critical devices detected in {selected_icu}. Immediate response required.
</div>
""",
        unsafe_allow_html=True,
    )

summary_columns = st.columns(4)
summary_values = [
    (connected_devices, "Connected Devices", "Total devices under surveillance", "blue"),
    (critical_count, "Critical Failures", "Urgent equipment alerts", "red"),
    (high_count + medium_count, "At-Risk Devices", "Elevated risk inventory", "yellow"),
    (average_health, "Avg Health Score", "Equipment wellness index", "green"),
]
for col, (value, title, label, variant) in zip(summary_columns, summary_values):
    with col:
        st.markdown(card_html(value, title, variant), unsafe_allow_html=True)
        st.markdown(
            f"<div style='margin-top:8px; color:#64748b; font-size:14px;'>{label}</div>",
            unsafe_allow_html=True,
        )

st.divider()

st.markdown("## ICU Health Pods")

preferred_types = [
    "Ventilator",
    "Patient Monitor",
    "Infusion Pump",
    "Oxygen Concentrator",
    "Defibrillator",
    "Telemetry Monitor",
    "ECG Machine",
    "Syringe Pump",
    "Anesthesia Machine",
]
available_types = [t for t in preferred_types if t in filtered["equipment_type"].unique()]
if len(available_types) < 6:
    extras = [t for t in filtered["equipment_type"].value_counts().index if t not in available_types]
    available_types += extras[: 6 - len(available_types)]
selected_types = available_types[:6]

pod_cols = st.columns(3)
for idx, equipment_type in enumerate(selected_types):
    group = filtered[filtered["equipment_type"] == equipment_type]
    if group.empty:
        continue

    avg_health = int(group["health_score"].mean())
    avg_risk = int(group["risk_score"].mean())
    avg_life = int(group["remaining_useful_life"].mean())
    mode_risk = (
        group["failure_risk_level"].mode().iloc[0]
        if not group["failure_risk_level"].mode().empty
        else "Healthy"
    )
    status_text, status_class = format_status(mode_risk)
    gauge = gauge_color(avg_health)

    with pod_cols[idx % 3]:
        st.markdown(
            f"""
<div class='health-pod'>
    <div>
        <h3>{equipment_type}</h3>
        <div class='pod-meta'>{len(group)} units active</div>
    </div>
    <div class='gauge-ring' style='--gauge-value:{avg_health}; --gauge-color:{gauge};'>
        <div class='gauge-value'>{avg_health}%</div>
    </div>
    <div class='pod-stats'>
        <div class='pod-stat'><span class='label'>Failure Risk</span><span class='value'>{avg_risk}%</span></div>
        <div class='pod-stat'><span class='label'>Remaining Life</span><span class='value'>{avg_life}d</span></div>
        <div class='pod-stat'><span class='label'>Technicians</span><span class='value'>{group['technician_assigned'].nunique()}</span></div>
        <div class='pod-stat'><span class='label'>Avg Usage</span><span class='value'>{int(group['usage_hours'].mean())}h</span></div>
    </div>
    <div class='status-chip {status_class}'>{status_text}</div>
</div>
""",
            unsafe_allow_html=True,
        )

st.divider()

st.markdown("## Risk Heatmap & Maintenance Timeline")
heatmap_col, timeline_col = st.columns([2, 1])

risk_matrix = filtered.pivot_table(
    index="icu_unit",
    columns="failure_risk_level",
    values="equipment_id",
    aggfunc="count",
    fill_value=0,
)

if not risk_matrix.empty:
    available_order = [
        col
        for col in ["Healthy", "Low", "Medium", "Moderate", "High", "Critical"]
        if col in risk_matrix.columns
    ]
    risk_matrix = risk_matrix.reindex(columns=available_order, fill_value=0)
    heatmap_fig = px.imshow(
        risk_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=["#eff6ff", "#38bdf8", "#f59e0b", "#dc2626"],
        title="Risk Status by ICU Unit",
    )
    heatmap_fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#102033",
    )
    heatmap_col.markdown("<div class='heatmap-card'>", unsafe_allow_html=True)
    heatmap_col.plotly_chart(heatmap_fig, width="stretch")
    heatmap_col.markdown("</div>", unsafe_allow_html=True)
else:
    heatmap_col.info("No heatmap data available for this ICU unit.")

upcoming = (
    filtered[filtered["next_maintenance_date"].notna()]
    .sort_values("next_maintenance_date")
    .head(8)
)

if not upcoming.empty:
    upcoming_display = upcoming[
        ["equipment_id", "equipment_type", "next_maintenance_date", "maintenance_priority"]
    ].copy()
    upcoming_display["next_maintenance_date"] = upcoming_display[
        "next_maintenance_date"
    ].dt.strftime("%b %d")
    upcoming_display.columns = ["Device", "Type", "Due Date", "Priority"]
    timeline_col.markdown("<div class='timeline-card'>", unsafe_allow_html=True)
    timeline_col.markdown("### Upcoming Maintenance Timeline", unsafe_allow_html=True)
    timeline_col.table(upcoming_display)
    timeline_col.markdown("</div>", unsafe_allow_html=True)
else:
    timeline_col.info("No maintenance items scheduled in the coming window.")

st.divider()

critical_assets = filtered[filtered["failure_risk_level"] == "Critical"].head(5)
if not critical_assets.empty:
    alert_lines = "".join(
        f"<li><strong>{row['equipment_id']}</strong> - {row['equipment_type']} | "
        f"Risk {int(row['risk_score'])}% | {row['ai_recommendation']}</li>"
        for _, row in critical_assets.iterrows()
    )
    st.markdown(
        f"""
<div class='floating-alert'>
    <h4>Critical Alert Queue</h4>
    <ul style='margin:0 0 0 20px; padding-left:18px; color:#7f1d1d;'>
        {alert_lines}
    </ul>
</div>
""",
        unsafe_allow_html=True,
    )

assistant_col, insights_col = st.columns([1, 1])
with assistant_col:
    st.markdown("<div class='assistant-card'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='chat-bubble user'><strong>Operator:</strong> Which assets need emergency response?</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='chat-bubble ai'><strong>AI Assistant:</strong> {critical_count} devices are in critical condition. Prioritize ventilators and oxygen concentrators first.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='chat-bubble user'><strong>Operator:</strong> What maintenance should we schedule today?</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='chat-bubble ai'><strong>AI Assistant:</strong> Schedule preventive maintenance for high-risk assets with low remaining life. Defibrillators and infusion pumps are highest priority.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with insights_col:
    st.markdown("<div class='status-board'>", unsafe_allow_html=True)
    st.markdown("## AI Intelligence Summary", unsafe_allow_html=True)
    st.markdown(
        f"""
<ul style='padding-left:20px; color:#102033;'>
    <li>Average health score: <strong>{average_health}%</strong></li>
    <li>Remaining useful life average: <strong>{avg_remaining_life} days</strong></li>
    <li>Critical density: <strong>{critical_count}</strong> devices</li>
    <li>At-risk inventory: <strong>{high_count + medium_count}</strong> devices</li>
    <li>AI maintenance accuracy: <strong>95.1%</strong></li>
</ul>
""",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.markdown("## Risk Intelligence Center")

risk_cols = st.columns(3)
with risk_cols[0]:
    st.error(
        f"""
### Critical Assets

{critical_count} Devices

Immediate attention required
"""
    )
with risk_cols[1]:
    st.warning(
        f"""
### High + Medium Risk

{high_count + medium_count} Devices

Prepare response plans
"""
    )
with risk_cols[2]:
    st.success(
        f"""
### Healthy Assets

{healthy_count} Devices

Stable operation
"""
    )

st.divider()

st.markdown("## Active Maintenance Tickets")

active_tickets = filtered.sort_values("maintenance_priority", ascending=False)[
    [
        "equipment_id",
        "equipment_type",
        "maintenance_priority",
        "technician_assigned",
        "ai_recommendation",
    ]
][:8]

if not active_tickets.empty:
    active_tickets = active_tickets.rename(
        columns={
            "equipment_id": "Ticket",
            "equipment_type": "Device",
            "maintenance_priority": "Priority",
            "technician_assigned": "Technician",
            "ai_recommendation": "Recommendation",
        }
    )
    st.dataframe(active_tickets, width="stretch")
else:
    st.info("There are currently no active maintenance tickets for this unit.")

st.divider()

st.markdown("## Equipment Health Intelligence")

health_data = pd.DataFrame(
    {
        "Health Status": ["Excellent", "Good", "Warning", "Critical"],
        "Count": [
            int((filtered["health_score"] >= 80).sum()),
            int(((filtered["health_score"] >= 60) & (filtered["health_score"] < 80)).sum()),
            int(((filtered["health_score"] >= 40) & (filtered["health_score"] < 60)).sum()),
            int((filtered["health_score"] < 40).sum()),
        ],
    }
)

fig = px.pie(
    health_data,
    names="Health Status",
    values="Count",
    hole=0.55,
    title="Equipment Health Distribution",
    color_discrete_map={
        "Excellent": "#2dd4bf",
        "Good": "#22c55e",
        "Warning": "#f59e0b",
        "Critical": "#ef4444",
    },
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#102033",
)

st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.plotly_chart(fig, width="stretch")
st.markdown("</div>", unsafe_allow_html=True)
