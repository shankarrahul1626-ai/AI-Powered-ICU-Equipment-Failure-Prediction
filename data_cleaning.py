import pandas as pd

df = pd.read_csv(
    "data/raw/icu_equipment.csv"
)

print(df.head())
print(df.shape)
print(df.info())
print("\nMissing Values")

print(df.isnull().sum())
duplicates = df.duplicated().sum()

print(
    f"Duplicate Rows: {duplicates}"
)
print(
    df.describe()
)
print("\nData Quality Report")

print(
    f"Rows : {df.shape[0]}"
)

print(
    f"Columns : {df.shape[1]}"
)

print(
    f"Missing Values : {df.isnull().sum().sum()}"
)

print(
    f"Duplicates : {df.duplicated().sum()}"
)
df.to_csv(
    "data/processed/cleaned_data.csv",
    index=False
)

print(
    "Cleaned Data Saved"
)
import pandas as pd

df = pd.read_csv(
    "data/raw/icu_equipment.csv"
)

print(df.head())

print(df.shape)

print(df.info())

print(df.isnull().sum())

print(df.duplicated().sum())

print(df.describe())

df.to_csv(
    "data/processed/cleaned_data.csv",
    index=False
)

print("Cleaned Data Saved")