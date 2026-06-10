import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("ggplot")
df = pd.read_csv(
    "data/processed/cleaned_data.csv"
)

print(df.head())
import os

os.makedirs(
    "reports/figures",
    exist_ok=True
)
plt.figure(figsize=(8,5))

sns.countplot(
    x="failure",
    data=df
)

plt.title(
    "Failure Distribution"
)

plt.savefig(
    "reports/figures/failure_distribution.png"
)

plt.show()
plt.figure(figsize=(8,5))

sns.histplot(
    df["temperature"],
    bins=30,
    kde=True
)

plt.title(
    "Temperature Distribution"
)

plt.savefig(
    "reports/figures/temperature_distribution.png"
)

plt.show()
plt.figure(figsize=(8,5))

sns.boxplot(
    x="failure",
    y="temperature",
    data=df
)

plt.title(
    "Temperature vs Failure"
)

plt.savefig(
    "reports/figures/temperature_vs_failure.png"
)

plt.show()
plt.figure(figsize=(8,5))

sns.boxplot(
    x="failure",
    y="error_count",
    data=df
)

plt.title(
    "Error Count vs Failure"
)

plt.savefig(
    "reports/figures/error_vs_failure.png"
)

plt.show()
plt.figure(figsize=(10,8))

corr = df.corr(
    numeric_only=True
)

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm"
)

plt.title(
    "Feature Correlation Heatmap"
)

plt.savefig(
    "reports/figures/correlation_heatmap.png"
)

plt.show()
plt.figure(figsize=(8,5))

sns.countplot(
    x="equipment_type",
    data=df
)

plt.xticks(rotation=45)

plt.title(
    "Equipment Type Distribution"
)

plt.savefig(
    "reports/figures/equipment_distribution.png"
)

plt.show()
plt.figure(figsize=(8,5))

sns.histplot(
    df["cpu_usage"],
    bins=20
)

plt.title(
    "CPU Usage Distribution"
)

plt.savefig(
    "reports/figures/cpu_usage_distribution.png"
)

plt.show()
failure_rate = (
    df["failure"].mean()
) * 100

print(
    f"Failure Rate: {failure_rate:.2f}%"
)
print("\nEDA Summary")

print(
    f"Total Records : {len(df)}"
)

print(
    f"Failure Rate : {failure_rate:.2f}%"
)

print(
    f"Average Temperature : {df['temperature'].mean():.2f}"
)

print(
    f"Average Error Count : {df['error_count'].mean():.2f}"
)