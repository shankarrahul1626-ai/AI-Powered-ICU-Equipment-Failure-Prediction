from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

# Load models
rf_model = joblib.load("models/random_forest.pkl")
rul_model = joblib.load("models/rul_model.pkl")


class EquipmentData(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    cpu_usage: int
    battery_health: int
    error_count: int
    usage_hours: int
    equipment_age: int
    health_score: float
    risk_score: float


@app.get("/")
def home():
    return {"message": "ICU Equipment Predictive Maintenance API"}


@app.post("/predict_failure")
def predict_failure(data: EquipmentData):
    return {"status": "working"}


@app.post("/predict_rul")
def predict_rul(data: EquipmentData):
    return {"status": "working"}