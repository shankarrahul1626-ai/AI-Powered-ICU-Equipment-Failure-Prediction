import pandas as pd

df = pd.read_csv(
    "data/features/feature_engineered_data.csv"
)
features = [

    "temperature",
    "vibration",
    "pressure",
    "cpu_usage",
    "battery_health",
    "error_count"

]
from sklearn.ensemble import IsolationForest

iso_model = IsolationForest(
    contamination=0.02,
    random_state=42
)

df["anomaly"] = iso_model.fit_predict(
    df[features]
)
print(
    df["anomaly"].value_counts()
)
anomalies = df[
    df["anomaly"] == -1
]

print(
    anomalies.head(10)
)
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))

plt.scatter(
    df["temperature"],
    df["vibration"],
    c=df["anomaly"]
)

plt.title(
    "Anomaly Detection"
)

plt.xlabel(
    "Temperature"
)

plt.ylabel(
    "Vibration"
)

plt.savefig(
    "reports/model_results/anomaly_detection.png"
)

plt.show()
df.to_csv(
    "data/features/anomaly_results.csv",
    index=False
)

print(
    "Anomaly Detection Completed"
)