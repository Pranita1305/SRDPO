from apscheduler.schedulers.background import BackgroundScheduler
from backend.db.collections.ride_demand_collection import insert_prediction
import joblib
import pandas as pd
import datetime

# Load models once
sarima_model = joblib.load("ml_models/sarima/sarima_model.pkl")
xgb_model = joblib.load("ml_models/xgboost/xgboost_model.pkl")
lstm_model = joblib.load("ml_models/lstm/lstm_model.h5")
lstm_scaler = joblib.load("ml_models/lstm/lstm_scaler.pkl")

# Define zones (you can fetch from DB later)
ZONES = [1, 2, 3, 4, 5]

def run_hourly_prediction():
    """Runs every hour to predict demand for all zones."""
    now = datetime.datetime.now()
    features_base = {
        "hour": now.hour,
        "day_of_week": now.weekday()
    }

    for zone_id in ZONES:
        features = pd.DataFrame({
            "hour": [features_base["hour"]],
            "day_of_week": [features_base["day_of_week"]],
            "zone_id": [zone_id]
        })

        try:
            xgb_pred = xgb_model.predict(features)[0]
            sarima_pred = sarima_model.forecast(steps=6).mean()
            lstm_input = lstm_scaler.transform(features)
            lstm_pred = lstm_model.predict(lstm_input)[0][0]

            final_pred = (xgb_pred * 0.4) + (sarima_pred * 0.4) + (lstm_pred * 0.2)

            insert_prediction(zone_id, final_pred)
            print(f"✅ Prediction stored for Zone {zone_id}: {final_pred:.2f}")

        except Exception as e:
            print(f"❌ Error for Zone {zone_id}: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_hourly_prediction, 'interval', hours=1)
    scheduler.start()
    print("🚀 APScheduler started - running hourly predictions")


from apscheduler.schedulers.background import BackgroundScheduler
from backend.db.collections.ride_demand_collection import insert_prediction
from backend.db.collections.surge_alerts_collection import insert_surge_alert
from backend.db.mongo_setup import db
import joblib
import pandas as pd
import datetime

# Load models once
sarima_model = joblib.load("ml_models/sarima/sarima_model.pkl")
xgb_model = joblib.load("ml_models/xgboost/xgboost_model.pkl")
lstm_model = joblib.load("ml_models/lstm/lstm_model.h5")
lstm_scaler = joblib.load("ml_models/lstm/lstm_scaler.pkl")
pricing_model = joblib.load("ml_models/xgboost/models/xgboost_traffic_model.pkl")

ZONES = [1, 2, 3, 4, 5]
DEMAND_THRESHOLD = 50  # adjust based on dataset patterns


def run_hourly_prediction():
    """Predicts ride demand for all zones and stores results."""
    now = datetime.datetime.now()
    features_base = {
        "hour": now.hour,
        "day_of_week": now.weekday()
    }

    for zone_id in ZONES:
        features = pd.DataFrame({
            "hour": [features_base["hour"]],
            "day_of_week": [features_base["day_of_week"]],
            "zone_id": [zone_id]
        })

        try:
            xgb_pred = xgb_model.predict(features)[0]
            sarima_pred = sarima_model.forecast(steps=6).mean()
            lstm_input = lstm_scaler.transform(features)
            lstm_pred = lstm_model.predict(lstm_input)[0][0]

            final_pred = (xgb_pred * 0.4) + (sarima_pred * 0.4) + (lstm_pred * 0.2)

            insert_prediction(zone_id, final_pred)
            print(f"✅ Demand Prediction stored for Zone {zone_id}: {final_pred:.2f}")

        except Exception as e:
            print(f"❌ Error for Zone {zone_id}: {e}")


def run_surge_alerts():
    """Checks latest predictions and inserts surge alerts if demand exceeds threshold."""
    latest_predictions = db.ride_demand_predictions.find().sort("timestamp", -1).limit(len(ZONES))

    for prediction in latest_predictions:
        zone_id = prediction["zone_id"]
        predicted_demand = prediction["predicted_demand"]

        if predicted_demand > DEMAND_THRESHOLD:
            try:
                # Generate surge pricing factor
                features = pd.DataFrame({
                    "zone_id": [zone_id],
                    "current_demand": [predicted_demand]
                })
                price_factor = pricing_model.predict(features)[0]

                insert_surge_alert(zone_id, predicted_demand, price_factor)
                print(f"🚨 Surge Alert: Zone {zone_id}, Demand {predicted_demand:.2f}, Price Factor {price_factor:.2f}")

            except Exception as e:
                print(f"❌ Surge alert error for Zone {zone_id}: {e}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_hourly_prediction, 'interval', hours=1)
    scheduler.add_job(run_surge_alerts, 'interval', hours=1, minutes=10)
    scheduler.start()
    print("🚀 APScheduler started - hourly predictions & surge alerts")
