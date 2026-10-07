import redis
import psycopg2
from neo4j import GraphDatabase
from kafka import KafkaProducer, KafkaConsumer
import json

from config.settings import settings
from src.common.logger import logger
from src.common.exceptions import DatabaseConnectionError


class DatabaseClients:
    """Singleton factory for persistent data layer connections."""

    _neo4j_driver = None
    _redis_client = None

    @classmethod
    def get_neo4j_driver(cls):
        """Returns or initializes the Neo4j Graph Database Driver."""
        if cls._neo4j_driver is None:
            try:
                cls._neo4j_driver = GraphDatabase.driver(
                    settings.neo4j_uri,
                    auth=(settings.neo4j_username, settings.neo4j_password)
                )
                logger.info("Successfully connected to Neo4j Graph Database.")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {str(e)}")
                raise DatabaseConnectionError(f"Neo4j Connection Failed: {str(e)}")
        return cls._neo4j_driver

    @classmethod
    def get_postgres_connection(cls):
        """Returns a new connection to PostgreSQL."""
        try:
            conn = psycopg2.connect(
                host=settings.postgres_host,
                port=settings.postgres_port,
                dbname=settings.postgres_db,
                user=settings.postgres_user,
                password=settings.postgres_password
            )
            return conn
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {str(e)}")
            raise DatabaseConnectionError(f"Postgres Connection Failed: {str(e)}")

    @classmethod
    def get_redis_client(cls):
        """Returns or initializes the Redis Cache Client."""
        if cls._redis_client is None:
            try:
                cls._redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
                logger.info("Successfully connected to Redis Cache.")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {str(e)}")
                raise DatabaseConnectionError(f"Redis Connection Failed: {str(e)}")
        return cls._redis_client

    @classmethod
    def get_kafka_producer(cls):
        """Returns a configured Kafka Producer instance."""
        try:
            producer = KafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap_servers.split(","),
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            return producer
        except Exception as e:
            logger.error(f"Failed to create Kafka Producer: {str(e)}")
            raise DatabaseConnectionError(f"Kafka Producer Creation Failed: {str(e)}")

    @classmethod
    def close_all(cls):
        """Gracefully closes open drivers."""
        if cls._neo4j_driver:
            cls._neo4j_driver.close()
            cls._neo4j_driver = None
            logger.info("Closed Neo4j Driver.")