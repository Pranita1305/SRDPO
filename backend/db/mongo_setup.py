from pymongo import MongoClient, ASCENDING

client = MongoClient("mongodb://localhost:27017")
db = client.srdapo

# Create collections if they don't exist
db.users.create_index([("email", ASCENDING)], unique=True)
db.ride_predictions.create_index([("timestamp", ASCENDING)])
db.ride_predictions.create_index([("zone_id", ASCENDING)])
db.zone_clusters.create_index([("zone_id", ASCENDING)], unique=True)
db.surge_alerts.create_index([("timestamp", ASCENDING)])
db.surge_alerts.create_index([("zone_id", ASCENDING)])

print("MongoDB collections and indexes created successfully.")
