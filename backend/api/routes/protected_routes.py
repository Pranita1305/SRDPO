from fastapi import APIRouter, Depends, HTTPException
from backend.auth.dependencies import get_current_user
from backend.db.models import RidePrediction, SurgeAlert
from pymongo import MongoClient
from datetime import datetime
from fastapi import APIRouter, Depends
from backend.auth.dependencies import get_current_user
from backend.utils.cache_manager import redis_client
import json

router = APIRouter()
client = MongoClient("mongodb://localhost:27017")
db = client.srdapo


@router.post("/upload-ride-data")
def upload_ride_data(data: RidePrediction, user=Depends(get_current_user)):
    if user['role'] not in ["admin", "analyst"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    db.ride_predictions.insert_one(data.dict())
    return {"msg": "Ride data uploaded successfully"}


@router.get("/view-surge-alerts")
def view_surge_alerts(user=Depends(get_current_user)):
    alerts = list(db.surge_alerts.find({}, {"_id": 0}))
    return {"alerts": alerts}


@router.post("/store-prediction")
def store_prediction(prediction: RidePrediction, user=Depends(get_current_user)):
    db.ride_predictions.insert_one(prediction.dict())
    return {"msg": "Prediction stored successfully"}


@router.post("/create-surge-alert")
def create_surge_alert(alert: SurgeAlert, user=Depends(get_current_user)):
    if user['role'] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create surge alerts")

    alert.timestamp = datetime.utcnow()
    db.surge_alerts.insert_one(alert.dict())
    return {"msg": "Surge alert created"}



router = APIRouter(prefix="/protected", tags=["Protected Routes"])

@router.get("/heatmap")
async def get_zone_heatmap(user=Depends(get_current_user)):
    cached_data = redis_client.get("zone_heatmap")
    if cached_data:
        return json.loads(cached_data)
    return {"message": "No cached heatmap found"}
