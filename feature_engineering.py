import pandas as pd
import numpy as np
import os

# =====================================================
# LOAD HOSPITAL DATASET
# =====================================================

df = pd.read_csv(
    "data/raw/hospital_equipment_data.csv"
)

print("Dataset Loaded")
print(df.shape)

# =====================================================
# FEATURE 1 - MAINTENANCE OVERDUE FLAG
# =====================================================

df["maintenance_overdue_flag"] = np.where(
    df["days_since_maintenance"] > 120,
    1,
    0
)

# =====================================================
# FEATURE 2 - HIGH RISK FLAG
# =====================================================

df["high_risk_flag"] = np.where(
    df["risk_score"] > 40,
    1,
    0
)

# =====================================================
# FEATURE 3 - CRITICAL EQUIPMENT FLAG
# =====================================================

df["critical_equipment_flag"] = np.where(
    df["criticality_score"] >= 80,
    1,
    0
)

# =====================================================
# FEATURE 4 - EQUIPMENT LIFECYCLE STAGE
# =====================================================

conditions = [

    df["remaining_useful_life"] > 10000,

    (df["remaining_useful_life"] <= 10000)
    &
    (df["remaining_useful_life"] > 5000),

    (df["remaining_useful_life"] <= 5000)
    &
    (df["remaining_useful_life"] > 2000),

    df["remaining_useful_life"] <= 2000
]

stages = [

    "Healthy",
    "Moderate",
    "Critical",
    "End Of Life"
]

df["equipment_lifecycle_stage"] = np.select(
    conditions,
    stages,
    default="Unknown"
)

# =====================================================
# FEATURE 5 - HEALTH CATEGORY
# =====================================================

health_conditions = [

    df["health_score"] >= 80,

    (df["health_score"] >= 60)
    &
    (df["health_score"] < 80),

    (df["health_score"] >= 40)
    &
    (df["health_score"] < 60),

    df["health_score"] < 40
]

health_labels = [

    "Excellent",
    "Good",
    "Warning",
    "Critical"
]

df["health_category"] = np.select(
    health_conditions,
    health_labels,
    default="Unknown"
)

# =====================================================
# FEATURE 6 - RISK CATEGORY
# =====================================================

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

df["risk_category"] = np.select(
    risk_conditions,
    risk_labels,
    default="Unknown"
)

# =====================================================
# SAVE FEATURE ENGINEERED DATA
# =====================================================

os.makedirs(
    "data/features",
    exist_ok=True
)

df.to_csv(
    "data/features/enterprise_feature_engineered_data.csv",
    index=False
)

print("\nFeature Engineering Completed Successfully")
print(df.shape)

print("\nNew Features Added:")
print(
    [
        "maintenance_overdue_flag",
        "high_risk_flag",
        "critical_equipment_flag",
        "equipment_lifecycle_stage",
        "health_category",
        "risk_category"
    ]
)

print("\nSample Data:")
print(df.head())