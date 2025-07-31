#Predict pricing surge

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from xgboost import XGBRegressor


# ---------------- Pricing Model Training ----------------
def load_and_clean_pricing_data(fares_path):
    df = pd.read_csv(fares_path, parse_dates=['pickup_datetime'])

    # Handle missing values
    df.fillna(method='ffill', inplace=True)

    # Feature engineering
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df['trip_distance'] = np.sqrt((df['dropoff_longitude'] - df['pickup_longitude'])**2 +
                                  (df['dropoff_latitude'] - df['pickup_latitude'])**2)

    return df

def train_pricing_model(df):
    features = ['hour', 'day_of_week', 'pickup_longitude', 'pickup_latitude',
                'dropoff_longitude', 'dropoff_latitude', 'passenger_count', 'trip_distance']
    X = df[features]
    y = df['fare_amount']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    xgb_price = XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=6)
    xgb_price.fit(X_train, y_train)

    preds = xgb_price.predict(X_test)
    print("Pricing Model RMSE:", np.sqrt(mean_squared_error(y_test, preds)))
    print("Pricing Model R2:", r2_score(y_test, preds))

    joblib.dump((xgb_price, scaler), 'ml_models/xgboost/pricing_model.pkl')

if __name__ == "__main__":
    pricing_df = load_and_clean_pricing_data('data/synthetic/trip_fares.csv')
    train_pricing_model(pricing_df)
    print("✅ Pricing model trained and saved successfully.")
