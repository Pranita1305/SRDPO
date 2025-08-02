# Fare prediction endpoints
from fastapi import APIRouter, Depends, HTTPException
from backend.auth.dependencies import get_current_user
import joblib
import pandas as pd
from backend.db.collections.surge_alerts_collection import insert_surge_alert

router = APIRouter(prefix="/pricing", tags=["Pricing Optimization"])

pricing_model = joblib.load("ml_models/xgboost/models/xgboost_traffic_model.pkl")

@router.post("/optimize")
async def optimize_pricing(zone_id: int, current_demand: float, user=Depends(get_current_user)):
    try:
        features = pd.DataFrame({
            "zone_id": [zone_id],
            "current_demand": [current_demand]
        })

        price_factor = pricing_model.predict(features)[0]

        insert_surge_alert(zone_id, current_demand, price_factor)

        return {"zone_id": zone_id, "suggested_price_factor": price_factor}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, Depends, HTTPException
from backend.auth.dependencies import get_current_user
from backend.db.collections.surge_alerts_collection import insert_surge_alert
import joblib
import pandas as pd

router = APIRouter(prefix="/pricing", tags=["Pricing Optimization"])

pricing_model = joblib.load("ml_models/xgboost/models/xgboost_traffic_model.pkl")

@router.post("/optimize")
async def optimize_pricing(zone_id: int, current_demand: float, user=Depends(get_current_user)):
    try:
        features = pd.DataFrame({
            "zone_id": [zone_id],
            "current_demand": [current_demand]
        })

        price_factor = pricing_model.predict(features)[0]
        insert_surge_alert(zone_id, current_demand, price_factor)

        return {"zone_id": zone_id, "suggested_price_factor": price_factor}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
