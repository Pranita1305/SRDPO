# Placeholder for LSTM training
#neural network model for sequential demand forecasting for time dependencies


import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from ml_models.utils.preprocessing import load_and_clean_data
from ml_models.utils.feature_engineering import add_time_features, add_lag_features

if __name__ == "__main__":
    df = load_and_clean_data('data/synthetic/ride_demand.csv', 'data/synthetic/weather_traffic.csv')
    df = add_time_features(df)
    df = add_lag_features(df)

    features = ['hour', 'day_of_week', 'is_weekend', 'weather_encoded',
                'vehicle_encoded', 'temperature_x', 'humidity_x', 'traffic_index_x',
                'hourly_vehicle_count', 'lag_1h', 'lag_2h', 'rolling_mean_3h']
    X = df[features].values
    y = df['ride_demand'].values

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    X_lstm = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

    X_train, X_test, y_train, y_test = train_test_split(X_lstm, y, test_size=0.2, random_state=42)

    model = Sequential([
        LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True),
        Dropout(0.2),
        LSTM(32),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test), verbose=1)

    model.save('ml_models/lstm/lstm_model.h5')
    joblib.dump(scaler, 'ml_models/lstm/lstm_scaler.pkl')
    print("LSTM model saved successfully.")
