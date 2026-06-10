import pandas as pd
import numpy as np
from datetime import datetime

# =====================================================
# CONFIGURATION
# =====================================================

np.random.seed(42)

n_samples = 10000

# =====================================================
# MASTER DATA
# =====================================================

hospitals = [
    "CityCare Multi-Speciality Hospital"
]

branches = [
    "Main Campus",
    "East Wing",
    "West Wing"
]

icu_units = [
    "Cardiac ICU",
    "Neuro ICU",
    "Pediatric ICU",
    "Emergency ICU",
    "Medical ICU",
    "Surgical ICU"
]

equipment_types = [
    "Ventilator",
    "Patient Monitor",
    "ECG Monitor",
    "Infusion Pump",
    "Syringe Pump",
    "Defibrillator",
    "Oxygen Concentrator",
    "Pulse Oximeter",
    "Anesthesia Machine",
    "CPAP Machine",
    "BiPAP Machine",
    "Telemetry Monitor",
    "Capnography Monitor",
    "Portable Ultrasound",
    "ABG Analyzer",
    "Portable X-Ray"
]

manufacturers = [
    "Philips Healthcare",
    "GE Healthcare",
    "Siemens Healthineers",
    "Drager",
    "Mindray",
    "Medtronic",
    "Baxter",
    "Fresenius Kabi"
]

technicians = [
    "Ravi Kumar",
    "Ananya Sharma",
    "Rahul Verma",
    "Priya Nair",
    "Arjun Patel",
    "Sneha Reddy",
    "Vikram Singh"
]

# =====================================================
# EQUIPMENT DATA
# =====================================================

equipment_id = np.arange(1000, 1000 + n_samples)

hospital_name = np.random.choice(
    hospitals,
    n_samples
)

hospital_branch = np.random.choice(
    branches,
    n_samples
)

icu_unit = np.random.choice(
    icu_units,
    n_samples
)

room_number = [
    f"ICU-{np.random.randint(100,150)}"
    for _ in range(n_samples)
]

bed_number = [
    f"B{np.random.randint(1,30):02d}"
    for _ in range(n_samples)
]

equipment_type = np.random.choice(
    equipment_types,
    n_samples
)

manufacturer = np.random.choice(
    manufacturers,
    n_samples
)

technician_assigned = np.random.choice(
    technicians,
    n_samples
)

# =====================================================
# SENSOR DATA
# =====================================================

temperature = np.random.normal(
    65,
    12,
    n_samples
)

vibration = np.random.normal(
    3,
    1.2,
    n_samples
)

pressure = np.random.normal(
    100,
    15,
    n_samples
)

cpu_usage = np.random.randint(
    10,
    100,
    n_samples
)

battery_health = np.random.randint(
    50,
    100,
    n_samples
)

error_count = np.random.poisson(
    5,
    n_samples
)

usage_hours = np.random.randint(
    100,
    20000,
    n_samples
)

equipment_age = np.random.randint(
    1,
    15,
    n_samples
)

days_since_maintenance = np.random.randint(
    1,
    180,
    n_samples
)

# =====================================================
# INSTALLATION & MAINTENANCE
# =====================================================

installation_date = np.random.choice(
    pd.date_range(
        start="2018-01-01",
        end="2025-01-01"
    ),
    n_samples
)

last_maintenance_date = np.random.choice(
    pd.date_range(
        start="2024-01-01",
        end="2025-12-31"
    ),
    n_samples
)

next_maintenance_date = np.random.choice(
    pd.date_range(
        start="2026-01-01",
        end="2026-12-31"
    ),
    n_samples
)

maintenance_cost = np.random.randint(
    1000,
    50000,
    n_samples
)

downtime_hours = np.random.randint(
    0,
    48,
    n_samples
)

# =====================================================
# WARRANTY & COMPLIANCE
# =====================================================

warranty_status = np.random.choice(
    [
        "In Warranty",
        "Expired"
    ],
    n_samples
)

compliance_status = np.random.choice(
    [
        "Compliant",
        "Pending Inspection",
        "Non-Compliant"
    ],
    n_samples
)

criticality_score = np.random.randint(
    1,
    100,
    n_samples
)

# =====================================================
# BUSINESS LOGIC
# =====================================================

health_score = (
    100
    - (temperature * 0.3)
    - (vibration * 4)
    - (error_count * 3)
)

health_score = np.clip(
    health_score,
    0,
    100
)

risk_score = (
    100 - health_score
)

remaining_useful_life = (
    15000
    - usage_hours
    + np.random.randint(
        -1000,
        1000,
        n_samples
    )
)

remaining_useful_life = np.clip(
    remaining_useful_life,
    500,
    15000
)

failure = np.where(
    (
        (temperature > 80)
        |
        (vibration > 5)
        |
        (error_count > 8)
        |
        (health_score < 45)
    ),
    1,
    0
)

maintenance_status = np.where(
    days_since_maintenance > 120,
    "Maintenance Due",
    "Normal"
)

# =====================================================
# DATAFRAME
# =====================================================

df = pd.DataFrame({

    "equipment_id": equipment_id,

    "hospital_name": hospital_name,
    "hospital_branch": hospital_branch,
    "icu_unit": icu_unit,
    "room_number": room_number,
    "bed_number": bed_number,

    "equipment_type": equipment_type,
    "manufacturer": manufacturer,

    "technician_assigned": technician_assigned,

    "installation_date": installation_date,
    "last_maintenance_date": last_maintenance_date,
    "next_maintenance_date": next_maintenance_date,

    "temperature": temperature,
    "vibration": vibration,
    "pressure": pressure,
    "cpu_usage": cpu_usage,
    "battery_health": battery_health,
    "error_count": error_count,

    "usage_hours": usage_hours,
    "equipment_age": equipment_age,
    "days_since_maintenance": days_since_maintenance,

    "maintenance_cost": maintenance_cost,
    "downtime_hours": downtime_hours,

    "warranty_status": warranty_status,
    "compliance_status": compliance_status,

    "criticality_score": criticality_score,

    "health_score": health_score,
    "risk_score": risk_score,

    "remaining_useful_life": remaining_useful_life,

    "failure": failure,

    "maintenance_status": maintenance_status
})

# =====================================================
# SAVE FILE
# =====================================================

output_path = "data/raw/hospital_equipment_data.csv"

df.to_csv(
    output_path,
    index=False
)

print("Dataset Generated Successfully")
print(df.shape)
print(df.head())
print(f"\nSaved To: {output_path}")