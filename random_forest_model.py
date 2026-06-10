import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/features/enterprise_feature_engineered_data.csv"
)

print("Dataset Shape:", df.shape)

# ==========================================
# FEATURES
# ==========================================

features = [

    "temperature",
    "vibration",
    "pressure",
    "cpu_usage",
    "battery_health",
    "error_count",
    "usage_hours",
    "equipment_age",
    "days_since_maintenance",

    "maintenance_cost",
    "downtime_hours",
    "criticality_score",

    "health_score",
    "risk_score",

    "maintenance_overdue_flag",
    "high_risk_flag",
    "critical_equipment_flag"
]

X = df[features]

y = df["failure"]

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# ==========================================
# EVALUATION
# ==========================================

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nAccuracy:", accuracy)

print(
    classification_report(
        y_test,
        predictions
    )
)

# ==========================================
# FEATURE IMPORTANCE
# ==========================================

importance_df = pd.DataFrame({

    "Feature": features,
    "Importance":
        model.feature_importances_

})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance_df)

# ==========================================
# SAVE MODEL
# ==========================================

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    model,
    "models/enterprise_random_forest.pkl"
)

print(
    "\nEnterprise Random Forest Saved"
)