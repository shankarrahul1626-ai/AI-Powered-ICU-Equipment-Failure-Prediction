import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    r2_score
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

y = df["remaining_useful_life"]

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

rul_model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

rul_model.fit(
    X_train,
    y_train
)

# ==========================================
# PREDICTIONS
# ==========================================

predictions = rul_model.predict(
    X_test
)

# ==========================================
# EVALUATION
# ==========================================

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)

print("\nRUL MODEL PERFORMANCE")
print("-" * 40)

print(
    f"Mean Absolute Error: {mae:.2f}"
)

print(
    f"R2 Score: {r2:.4f}"
)

# ==========================================
# FEATURE IMPORTANCE
# ==========================================

importance_df = pd.DataFrame({

    "Feature": features,
    "Importance":
        rul_model.feature_importances_

})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance_df)

# ==========================================
# CREATE REPORT FOLDER
# ==========================================

os.makedirs(
    "reports/model_results",
    exist_ok=True
)

# ==========================================
# ACTUAL VS PREDICTED
# ==========================================

plt.figure(figsize=(10, 6))

plt.scatter(
    y_test,
    predictions,
    alpha=0.5
)

plt.xlabel(
    "Actual Remaining Useful Life"
)

plt.ylabel(
    "Predicted Remaining Useful Life"
)

plt.title(
    "Enterprise RUL Prediction"
)

plt.savefig(
    "reports/model_results/enterprise_rul_prediction.png"
)

plt.close()

# ==========================================
# SAVE MODEL
# ==========================================

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    rul_model,
    "models/enterprise_rul_model.pkl"
)

print(
    "\nEnterprise RUL Model Saved Successfully"
)