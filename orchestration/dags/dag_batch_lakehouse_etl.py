from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'stern_watch_data_eng',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': True,
    'email': ['alerts@mercedes-benz.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dag_batch_lakehouse_etl',
    default_args=default_args,
    description='Nightly Lakehouse ELT for SAP iDocs and Customs Manifests',
    schedule_interval='0 2 * * *',  # Runs daily at 02:00 AM UTC
    catchup=False,
    tags=['lakehouse', 'pyspark', 'etl'],
) as dag:

    extract_sap_idocs = BashOperator(
        task_id='extract_sap_idocs',
        bash_command='python /opt/airflow/dags/scripts/extract_sap.py'
    )

    parse_customs_pdfs = BashOperator(
        task_id='parse_customs_pdfs',
        bash_command='python /opt/airflow/dags/scripts/parse_manifests.py'
    )

    pyspark_delta_transform = BashOperator(
        task_id='pyspark_delta_transform',
        bash_command='spark-submit --master local[*] /opt/airflow/dags/scripts/lakehouse_transform.py'
    )

    [extract_sap_idocs, parse_customs_pdfs] >> pyspark_delta_transform