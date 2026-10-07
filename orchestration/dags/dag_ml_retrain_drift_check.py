from datetime import datetime, timedelta
from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator, BranchPythonOperator  # type: ignore

default_args = {
    'owner': 'stern_watch_mlops',
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
}

def evaluate_data_drift():
    """Checks KS-Test p-value from MLops monitor."""
    p_value = 0.08  # Example evaluated value
    if p_value < 0.05:
        return 'retrain_xgboost_model'
    return 'skip_retrain_task'

def retrain_model():
    print("Retraining XGBoost Delay Predictor on updated 30-day telemetry window...")

def skip_retrain():
    print("No significant drift detected. Skipping retrain cycle.")

with DAG(
    'dag_ml_retrain_drift_check',
    default_args=default_args,
    description='Automated ML Model Drift Check & Conditional Retrain',
    schedule_interval='0 6 * * 0',  # Runs weekly on Sunday at 06:00 AM UTC
    catchup=False,
    tags=['mlops', 'xgboost', 'drift'],
) as dag:

    check_drift = BranchPythonOperator(
        task_id='check_feature_drift',
        python_callable=evaluate_data_drift
    )

    retrain_task = PythonOperator(
        task_id='retrain_xgboost_model',
        python_callable=retrain_model
    )

    skip_task = PythonOperator(
        task_id='skip_retrain_task',
        python_callable=skip_retrain
    )

    check_drift >> [retrain_task, skip_task]