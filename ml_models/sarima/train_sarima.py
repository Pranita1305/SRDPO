# Placeholder for SARIMA training
#for zone wise clusters and hourly demand

import joblib
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from ml_models.utils.preprocessing import load_and_clean_data
from ml_models.utils.feature_engineering import add_time_features

def train_sarima_for_zone(df, zone_id):
    zone_data = df[df['zone_id'] == zone_id].set_index('datetime')['ride_demand']
    model = SARIMAX(zone_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 24))
    sarima_model = model.fit(disp=False)
    joblib.dump(sarima_model, f'ml_models/sarima/sarima_zone_{zone_id}.pkl')
    print(f"SARIMA model trained for Zone {zone_id}")

if __name__ == "__main__":
    df = load_and_clean_data('data/synthetic/ride_demand.csv', 'data/synthetic/weather_traffic.csv')
    df = add_time_features(df)

    for zone in df['zone_id'].unique():
        train_sarima_for_zone(df, zone)
