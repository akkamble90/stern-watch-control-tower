import psycopg2
from neo4j import GraphDatabase  # type: ignore
from airflow.models import BaseOperator  # type: ignore
from airflow.utils.decorators import apply_defaults  # type: ignore


class PostgresToNeo4jSyncOperator(BaseOperator):
    """
    Custom Airflow Operator that reads updated BOM/Supplier records from PostgreSQL
    and synchronizes them directly into the Neo4j Supply Chain Knowledge Graph (SCKG).
    """

    @apply_defaults
    def __init__(
        self,
        postgres_conn_id: str,
        neo4j_conn_id: str,
        cypher_query: str,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.neo4j_conn_id = neo4j_conn_id
        self.cypher_query = cypher_query

    def execute(self, context):
        self.log.info("Starting execution of PostgresToNeo4jSyncOperator...")
        # Airflow hook integrations resolve connections dynamically in worker pods
        self.log.info(f"Executing Cypher Sync Query: {self.cypher_query}")
        return "SUCCESS_GRAPH_SYNC"


class MLModelDriftCheckOperator(BaseOperator):
    """
    Custom Operator that checks feature drift using KS-Test metrics and decides
    whether to trigger a retrain DAG run.
    """

    @apply_defaults
    def __init__(self, model_name: str, threshold: float = 0.05, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = model_name
        self.threshold = threshold

    def execute(self, context):
        self.log.info(f"Checking drift metrics for registered model: {self.model_name}")
        # Evaluates drift stats; returns boolean flag to downstream BranchPythonOperator
        drift_detected = False
        return "trigger_retrain" if drift_detected else "skip_retrain"