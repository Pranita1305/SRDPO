from backend.db.mongo_setup import db
from datetime import datetime

def insert_prediction(zone_id: int, predicted_demand: float):
    """Insert predicted demand for a zone into MongoDB."""
    record = {
        "zone_id": zone_id,
        "predicted_demand": predicted_demand,
        "timestamp": datetime.utcnow()
    }
    db.ride_demand_predictions.insert_one(record)
    return record
