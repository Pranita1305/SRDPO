from fastapi import APIRouter, Depends
from backend.auth.dependencies import get_current_user
from backend.db.mongo_setup import db

router = APIRouter(prefix="/dashboard", tags=["Dashboard Data"])


@router.get("/data")
async def get_dashboard_data(user=Depends(get_current_user)):
    predictions = list(db.ride_demand_predictions.find({}, {"_id": 0}).sort("timestamp", -1).limit(50))
    surge_alerts = list(db.surge_alerts.find({}, {"_id": 0}).sort("timestamp", -1).limit(50))

    return {
        "predictions": predictions,
        "surge_alerts": surge_alerts
    }
