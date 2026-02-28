from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Input data model
class SensorData(BaseModel):
    sound_score: float      # 0.0 to 1.0 from YAMNet
    motion_spike: bool      # True if violent motion detected
    hour: int               # Current hour 0-23
    location_anomaly: bool  # True if unusual location

def calculate_risk(data: SensorData) -> float:
    # Weights for each signal
    sound_weight    = 0.40
    motion_weight   = 0.30
    time_weight     = 0.20
    location_weight = 0.10

    # Time score — night hours (10pm to 5am) are riskier
    if data.hour >= 22 or data.hour <= 5:
        time_score = 1.0
    elif data.hour >= 20 or data.hour <= 7:
        time_score = 0.5
    else:
        time_score = 0.1

    motion_score   = 1.0 if data.motion_spike else 0.0
    location_score = 1.0 if data.location_anomaly else 0.0

    # Final weighted risk score
    risk = (
        data.sound_score   * sound_weight +
        motion_score       * motion_weight +
        time_score         * time_weight +
        location_score     * location_weight
    )

    return round(risk, 3)

@app.post("/analyze")
def analyze(data: SensorData):
    risk_score = calculate_risk(data)
    trigger_sos = risk_score >= 0.7

    return {
        "risk_score": risk_score,
        "trigger_sos": trigger_sos,
        "message": "🚨 DANGER - Triggering SOS!" if trigger_sos else "✅ Safe"
    }

@app.get("/")
def root():
    return {"status": "RakshaAI Risk Engine is running"}