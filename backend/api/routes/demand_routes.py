# Demand prediction endpoints
from fastapi import APIRouter, Depends, HTTPException
from backend.auth.dependencies import get_current_user
import joblib
import pandas as pd
import datetime
from backend.db.collections.ride_demand_collection import insert_prediction

router = APIRouter(prefix="/demand", tags=["Demand Prediction"])

# Load models
sarima_model = joblib.load("ml_models/sarima/sarima_model.pkl")
xgb_model = joblib.load("ml_models/xgboost/xgboost_model.pkl")
lstm_model = joblib.load("ml_models/lstm/lstm_model.h5")
lstm_scaler = joblib.load("ml_models/lstm/lstm_scaler.pkl")

@router.post("/predict")
async def predict_demand(zone_id: int, forecast_hours: int = 6, user=Depends(get_current_user)):
    try:
        # Example feature preparation
        now = datetime.datetime.now()
        features = pd.DataFrame({
            "hour": [now.hour],
            "day_of_week": [now.weekday()],
            "zone_id": [zone_id]
        })

        # XGBoost prediction
        xgb_pred = xgb_model.predict(features)[0]

        # SARIMA prediction
        sarima_forecast = sarima_model.forecast(steps=forecast_hours)
        sarima_pred = sarima_forecast.mean()

        # (Optional) LSTM prediction
        lstm_input = lstm_scaler.transform(features)
        lstm_pred = lstm_model.predict(lstm_input)[0][0]

        # Hybrid forecast (weighted average)
        final_pred = (xgb_pred * 0.4) + (sarima_pred * 0.4) + (lstm_pred * 0.2)

        # Save prediction to MongoDB
        insert_prediction(zone_id, final_pred)

        return {"zone_id": zone_id, "predicted_demand": final_pred}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi import APIRouter, Depends, HTTPException
from backend.auth.dependencies import get_current_user
from backend.db.collections.ride_demand_collection import insert_prediction
import joblib
import pandas as pd
import datetime

router = APIRouter(prefix="/demand", tags=["Demand Prediction"])

# Load trained models
sarima_model = joblib.load("ml_models/sarima/sarima_model.pkl")
xgb_model = joblib.load("ml_models/xgboost/xgboost_model.pkl")
lstm_model = joblib.load("ml_models/lstm/lstm_model.h5")
lstm_scaler = joblib.load("ml_models/lstm/lstm_scaler.pkl")

@router.post("/predict")
async def predict_demand(zone_id: int, forecast_hours: int = 6, user=Depends(get_current_user)):
    try:
        now = datetime.datetime.now()
        features = pd.DataFrame({
            "hour": [now.hour],
            "day_of_week": [now.weekday()],
            "zone_id": [zone_id]
        })

        xgb_pred = xgb_model.predict(features)[0]
        sarima_pred = sarima_model.forecast(steps=forecast_hours).mean()

        lstm_input = lstm_scaler.transform(features)
        lstm_pred = lstm_model.predict(lstm_input)[0][0]

        final_pred = (xgb_pred * 0.4) + (sarima_pred * 0.4) + (lstm_pred * 0.2)

        insert_prediction(zone_id, final_pred)

        return {"zone_id": zone_id, "predicted_demand": final_pred}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
