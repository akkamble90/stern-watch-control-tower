import mlflow  # type: ignore
import pandas as pd
from scipy.stats import ks_2samp
from src.common.logger import logger
from src.common.exceptions import ControlTowerBaseException


class DataDriftMonitor:
    """Monitors feature distribution drift using two-sample Kolmogorov-Smirnov test."""

    def __init__(self, p_value_threshold: float = 0.05):
        self.p_value_threshold = p_value_threshold

    def evaluate_feature_drift(
        self, baseline_series: pd.Series, current_series: pd.Series, feature_name: str
    ) -> dict:
        """Executes KS-Test on a numerical feature to detect distribution shifts."""
        try:
            # Drop NaNs for statistical validity
            base_clean = baseline_series.dropna()
            curr_clean = current_series.dropna()

            # Execute Kolmogorov-Smirnov Test
            ks_stat, p_value = ks_2samp(base_clean, curr_clean)
            drift_detected = p_value < self.p_value_threshold

            results = {
                "feature_name": feature_name,
                "ks_statistic": float(ks_stat),
                "p_value": float(p_value),
                "drift_detected": bool(drift_detected),
            }

            logger.info(
                f"Drift Evaluation [{feature_name}]: KS-Stat={ks_stat:.4f}, p-val={p_value:.4f}, Drift={drift_detected}"
            )

            # Log to active MLflow run if available
            if mlflow.active_run():
                mlflow.log_metric(f"drift_ks_stat_{feature_name}", ks_stat)
                mlflow.log_metric(f"drift_p_value_{feature_name}", p_value)
                mlflow.log_param(f"drift_detected_{feature_name}", drift_detected)

            return results

        except Exception as e:
            logger.error(f"Failed to calculate drift for {feature_name}: {str(e)}")
            raise ControlTowerBaseException(f"Drift Monitoring Error: {str(e)}")


if __name__ == "__main__":
    import numpy as np

    # Example test harness simulating baseline vs drifted sea state telemetry
    monitor = DataDriftMonitor()
    baseline = pd.Series(np.random.normal(loc=15.0, scale=2.0, size=1000))  # Baseline transit speeds
    drifted = pd.Series(np.random.normal(loc=8.0, scale=4.0, size=1000))   # Storm delay speeds

    res = monitor.evaluate_feature_drift(baseline, drifted, feature_name="shipment_speed_knots")
    print(f"Drift Result: {res}")