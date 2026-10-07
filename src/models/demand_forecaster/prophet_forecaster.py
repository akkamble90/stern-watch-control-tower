import pandas as pd
from prophet import Prophet

def forecast_part_demand(historical_df: pd.DataFrame, periods: int = 30) -> pd.DataFrame:
    """Historical DF must contain 'ds' (date) and 'y' (demand quantity)."""
    m = Prophet()
    m.fit(historical_df)
    future = m.make_future_dataframe(periods=periods)
    forecast = m.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]