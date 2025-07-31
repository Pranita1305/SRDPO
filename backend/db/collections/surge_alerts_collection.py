from backend.db.mongo_setup import db
from datetime import datetime

def insert_surge_alert(zone_id: int, current_demand: float, price_factor: float):
    """Insert surge pricing alert for a zone into MongoDB."""
    record = {
        "zone_id": zone_id,
        "current_demand": current_demand,
        "suggested_price_factor": price_factor,
        "timestamp": datetime.utcnow()
    }
    db.surge_alerts.insert_one(record)
    return record
