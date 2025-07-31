# Feature engineering utilities
#Advanced feature generation (lags, rolling averages, weather impact, holiday features)
#Called inside preprocessing and training scripts to enrich datasets

import pandas as pd
import numpy as np

def add_time_features(df):
    """Add hour, weekday, weekend indicators"""
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    return df

def add_lag_features(df, group_col='zone_id', target_col='ride_demand'):
    """Add lag features and rolling averages"""
    df['lag_1h'] = df.groupby(group_col)[target_col].shift(1)
    df['lag_2h'] = df.groupby(group_col)[target_col].shift(2)
    df['rolling_mean_3h'] = df.groupby(group_col)[target_col].transform(lambda x: x.rolling(3).mean())
    df.fillna(0, inplace=True)
    return df
