# ml_models/xgboost/train_xgboost.py
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib
import os

from ml_models.utils.feature_engineering import add_time_features

# Load dataset
df = pd.read_csv("data/synthetic/weather_traffic.csv")

# Convert datetime
df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

# Feature engineering
df = add_time_features(df)

# Encode weather (one-hot)
df = pd.get_dummies(df, columns=["weather"], drop_first=True)

# Drop original datetime (already encoded into hour/day features)
df = df.drop("datetime", axis=1)

# Define features and target
X = df.drop("traffic_index", axis=1)
y = df["traffic_index"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost
model = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, preds))
print("XGBoost RMSE:", rmse)

# Save model
os.makedirs("ml_models/xgboost/models", exist_ok=True)
joblib.dump(model, "ml_models/xgboost/models/xgboost_traffic_model.pkl")
print("XGBoost model saved successfully.")
