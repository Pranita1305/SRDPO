import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def load_and_clean_data(ride_path, weather_path):
    ride_df = pd.read_csv(ride_path, parse_dates=['datetime'])
    weather_df = pd.read_csv(weather_path, parse_dates=['datetime'])

    df = ride_df.merge(weather_df, on=['datetime', 'zone_id'], how='left')
    df.fillna(method='ffill', inplace=True)

    for col in ['hourly_vehicle_count', 'ride_demand']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]

    le_weather = LabelEncoder()
    df['weather_encoded'] = le_weather.fit_transform(df['weather_x'])

    le_vehicle = LabelEncoder()
    df['vehicle_encoded'] = le_vehicle.fit_transform(df['vehicle_type'])

    return df
