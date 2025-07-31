# ml_models/zone_clustering/train_zone_clustering.py
import pandas as pd
from sklearn.cluster import KMeans
import joblib
import os

def train_zone_clustering(data_path):
    df = pd.read_csv(data_path)

    # Map correct columns
    df = df.rename(columns={
        'lat': 'latitude',
        'lon': 'longitude',
        'avg_daily_demand': 'avg_demand'
    })

    # If traffic_index is missing, create a synthetic one
    if 'traffic_index' not in df.columns:
        df['traffic_index'] = df['avg_demand'] * 0.1  # simple heuristic

    features = ['latitude', 'longitude', 'avg_demand', 'traffic_index']
    X = df[features]

    kmeans = KMeans(n_clusters=10, random_state=42)
    df['cluster'] = kmeans.fit_predict(X)

    os.makedirs("ml_models/zone_clustering/models", exist_ok=True)
    joblib.dump(kmeans, "ml_models/zone_clustering/models/zone_cluster_model.pkl")
    df.to_csv("data/processed/zone_clusters_with_labels.csv", index=False)

    print("Zone clustering model trained and saved.")

if __name__ == "__main__":
    train_zone_clustering("data/synthetic/zone_clusters.csv")
