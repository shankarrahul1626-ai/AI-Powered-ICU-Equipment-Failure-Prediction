import pandas as pd
import numpy as np

# ====================================
# LOAD DATA
# ====================================

df = pd.read_csv(
    "data/features/enterprise_feature_engineered_data.csv"
)

# ====================================
# RISK LEVEL
# ====================================

risk_conditions = [

    df["risk_score"] < 20,

    (df["risk_score"] >= 20)
    &
    (df["risk_score"] < 40),

    (df["risk_score"] >= 40)
    &
    (df["risk_score"] < 60),

    df["risk_score"] >= 60

]

risk_labels = [

    "Low",
    "Medium",
    "High",
    "Critical"
]

df["failure_risk_level"] = np.select(
    risk_conditions,
    risk_labels,
    default="Medium"
)

# ====================================
# MAINTENANCE PRIORITY
# ====================================

priority_conditions = [

    df["criticality_score"] < 40,

    (df["criticality_score"] >= 40)
    &
    (df["criticality_score"] < 70),

    (df["criticality_score"] >= 70)
    &
    (df["criticality_score"] < 90),

    df["criticality_score"] >= 90

]

priority_labels = [

    "Routine",
    "Scheduled",
    "Urgent",
    "Emergency"
]

df["maintenance_priority"] = np.select(
    priority_conditions,
    priority_labels,
    default="Routine"
)

# ====================================
# COST IMPACT
# ====================================

cost_conditions = [

    df["downtime_hours"] < 8,

    (df["downtime_hours"] >= 8)
    &
    (df["downtime_hours"] < 24),

    df["downtime_hours"] >= 24

]

cost_labels = [

    "Low Cost",
    "Medium Cost",
    "High Cost"
]

df["downtime_cost_impact"] = np.select(
    cost_conditions,
    cost_labels,
    default="Low Cost"
)

# ====================================
# AI RECOMMENDATIONS
# ====================================

recommendations = []

for _, row in df.iterrows():

    if row["failure_risk_level"] == "Critical":
        recommendations.append(
            "Immediate maintenance required"
        )

    elif row["failure_risk_level"] == "High":
        recommendations.append(
            "Schedule technician inspection"
        )

    elif row["maintenance_status"] == "Maintenance Due":
        recommendations.append(
            "Perform preventive maintenance"
        )

    else:
        recommendations.append(
            "Equipment operating normally"
        )

df["ai_recommendation"] = recommendations

# ====================================
# SAVE
# ====================================

df.to_csv(
    "data/features/risk_intelligence_data.csv",
    index=False
)

print("Risk Intelligence Engine Completed")

print(df[
    [
        "equipment_id",
        "failure_risk_level",
        "maintenance_priority",
        "downtime_cost_impact",
        "ai_recommendation"
    ]
].head())