# churn_pipeline.py
import math
from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="Customer Churn Prediction Pipeline", version="1.0.0")

class ChurnRequest(BaseModel):
    user_id: str
    tenure_months: int = Field(..., ge=0)
    monthly_charges: float = Field(..., ge=0)
    support_tickets_opened: int = Field(..., ge=0)

@app.post("/api/v1/predict/churn", status_code=status.HTTP_200_OK)
async def predict_customer_churn(request: ChurnRequest):
    score_facteur = (request.support_tickets_opened * 0.25) + (request.monthly_charges * 0.002) - (request.tenure_months * 0.01)
    churn_probability = round(1 / (1 + math.exp(-score_facteur)), 3)
    
    risk_level = "Low"
    if churn_probability > 0.7:
        risk_level = "Critical"
    elif churn_probability > 0.4:
        risk_level = "Medium"
        
    return {
        "user_id": request.user_id,
        "churn_probability": churn_probability,
        "risk_level": risk_level,
        "action_recommended": "Trigger Retention Campaign" if risk_level in ["Medium", "Critical"] else "Maintain Standard Flow"
    }
