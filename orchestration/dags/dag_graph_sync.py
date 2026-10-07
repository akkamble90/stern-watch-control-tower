from datetime import datetime, timedelta
from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore

default_args = {
    'owner': 'stern_watch_data_eng',
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

def sync_neo4j_nodes():
    """Triggers Neo4j Graph synchronization for Tier-1 to Tier-3 relationships."""
    print("Synchronizing Neo4j SCKG nodes with Lakehouse master tables...")

with DAG(
    'dag_graph_sync',
    default_args=default_args,
    description='Synchronizes Neo4j Supply Chain Knowledge Graph',
    schedule_interval='0 */4 * * *',  # Runs every 4 hours
    catchup=False,
    tags=['neo4j', 'graph', 'sckg'],
) as dag:

    sync_graph_task = PythonOperator(
        task_id='sync_neo4j_sckg',
        python_callable=sync_neo4j_nodes
    )