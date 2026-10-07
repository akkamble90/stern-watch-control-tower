import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Core Application Settings.
    Parses and validates environment variables from .env file or system environment.
    """

    # LLM Engine
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    llm_model_name: str = Field("llama-3.3-70b-versatile", env="LLM_MODEL_NAME")
    tavily_api_key: str = Field(..., env="TAVILY_API_KEY")

    # POWER BI & AZURE AD OAUTH 2.0
    powerbi_tenant_id: str = Field(..., env="POWERBI_TENANT_ID")
    powerbi_client_id: str = Field(..., env="POWERBI_CLIENT_ID")
    powerbi_client_secret: str = Field(..., env="POWERBI_CLIENT_SECRET")
    powerbi_workspace_id: str = Field(..., env="POWERBI_WORKSPACE_ID")
    powerbi_dashboard_id: Optional[str] = Field(None, env="POWERBI_DASHBOARD_ID")
    powerbi_report_id: Optional[str] = Field(None, env="POWERBI_REPORT_ID")

    #KNOWLEDGE GRAPH & DATABASES
    neo4j_uri: str = Field("bolt://localhost:7687", env="NEO4J_URI")
    neo4j_username: str = Field("neo4j", env="NEO4J_USERNAME")
    neo4j_password: str = Field(..., env="NEO4J_PASSWORD")

    postgres_host: str = Field("localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")
    postgres_db: str = Field("control_tower_db", env="POSTGRES_DB")
    postgres_user: str = Field("postgres", env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")

    #STREAMING & MESSAGING BUS
    kafka_bootstrap_servers: str = Field("localhost:9092", env="KAFKA_BOOTSTRAP_SERVERS")
    kafka_telemetry_topic: str = Field("raw_freight_telemetry", env="KAFKA_TELEMETRY_TOPIC")
    kafka_alerts_topic: str = Field("supply_chain_alerts", env="KAFKA_ALERTS_TOPIC")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")

    #SECURITY & HUMAN-IN-THE-LOOP
    hitl_hmac_secret_key: str = Field(..., env="HITL_HMAC_SECRET_KEY")
    encryption_aes_key: str = Field(..., env="ENCRYPTION_AES_KEY")

    # Pydantic Config to read .env file automatically
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def postgres_connection_string(self) -> str:
        """Constructs PostgreSQL SQLAlchemy connection string."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


# Singleton Instance
settings = Settings()