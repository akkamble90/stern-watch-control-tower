import requests
from datetime import datetime, timedelta
from airflow import DAG  # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore

default_args = {
    'owner': 'stern_watch_bi',
    'start_date': datetime(2026, 1, 1),
    'retries': 2,
}

def trigger_powerbi_refresh():
    """Calls Power BI REST API to trigger workspace dataset refresh."""
    print("Sending REST trigger to Power BI Workspace dataset refresh API...")

with DAG(
    'dag_powerbi_dataset_refresh',
    default_args=default_args,
    description='Triggers Power BI Executive Dashboard Dataset Refresh',
    schedule_interval='30 2 * * *',  # Runs daily at 02:30 AM UTC (after ETL)
    catchup=False,
    tags=['powerbi', 'analytics', 'refresh'],
) as dag:

    refresh_pbi = PythonOperator(
        task_id='trigger_powerbi_api_refresh',
        python_callable=trigger_powerbi_refresh
    )