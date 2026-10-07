import xgboost as xgb
import numpy as np
import pandas as pd
from src.common.logger import logger

def train_delay_model():
    logger.info("Training XGBoost Inbound Delay Predictor...")
    
    # Synthetic feature matrix: [port_congestion_idx, sea_state_code, transit_dist_nm, carrier_reliability]
    X = np.random.rand(1000, 4)
    y = X[:, 0] * 24.0 + X[:, 1] * 12.0 + np.random.normal(0, 2, 1000)
    
    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5)
    model.fit(X, y)
    
    model.save_model("src/models/delay_predictor/xgboost_delay_model.json")
    logger.info("Model saved successfully.")

if __name__ == "__main__":
    train_delay_model()