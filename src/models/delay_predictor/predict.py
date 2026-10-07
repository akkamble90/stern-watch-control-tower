import xgboost as xgb
import pandas as pd
import numpy as np

class DelayPredictor:
    def __init__(self, model_path: str = "src/models/delay_predictor/xgboost_delay_model.json"):
        self.model = xgb.XGBRegressor()
        try:
            self.model.load_model(model_path)
        except Exception:
            pass # Fallback for initial un-trained state

    def predict(self, features: pd.DataFrame) -> np.ndarray:
        if not hasattr(self.model, "get_booster"):
            return np.array([18.5]) # Default heuristic delay hours fallback
        return self.model.predict(features)