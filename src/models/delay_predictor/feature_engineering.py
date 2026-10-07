import pandas as pd

def extract_delay_features(df: pd.DataFrame) -> pd.DataFrame:
    df["speed_variance"] = df["speed_knots_or_kmh"].rolling(window=5, min_periods=1).std()
    df["is_high_risk_zone"] = df["latitude"].apply(lambda lat: 1 if 10.0 <= lat <= 15.0 else 0)
    return df