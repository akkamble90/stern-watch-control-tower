##  Supply Chain Telemetry Control Tower & Agentic Command Center

An enterprise-grade, real-time supply chain monitoring platform and multi-agent AI risk engine. The system ingests high-frequency vehicle telemetry and warehouse inventory events via **Apache Kafka**, processes micro-batches with **PySpark Structured Streaming**, persists operational state to **PostgreSQL**, and renders an executive control tower in **Streamlit** embedded with **Power BI** interactive visual reports and a **LangGraph** multi-agent risk assessment command center.

---

##  Key Features

###  1. Real-Time Telemetry & Streaming Pipeline
* **Kafka Event Ingestion**: High-throughput telemetry producer streaming vehicle GPS, speed, and container thermal sensors[cite: 5, 11].
* **PySpark Structured Streaming**: Real-time schema enforcement, geofencing, and thermal anomaly enrichment with micro-batch JDBC upserts into PostgreSQL[cite: 5, 11].
* **Automated Data Quality & Drift Monitoring**: Integrated Great Expectations validation suites and Kolmogorov-Smirnov statistical data drift monitoring[cite: 6, 7].

### 2. Agentic Supply Chain Orchestration (LangGraph)
* **Multi-Agent State Machine**: Cyclical LangGraph architecture featuring specialized Researcher, Risk Analyst, and Critic verification nodes[cite: 5, 6, 9].
* **Hybrid Knowledge RAG**: Seamless integration with Neo4j knowledge graphs, `pgvector` similarity search, and SAP BAPI ERP connectors[cite: 8, 9, 11].
* **Human-In-The-Loop (HITL) Guardrails**: Cryptographic HMAC signature generation and role-based sign-offs for critical automated decisions[cite: 6, 8, 10].

###  3. Executive Control Tower UI & Power BI Integration
* **Embedded Analytics**: Live, authenticated Power BI report iFrames rendered smoothly inside Streamlit (`powerbi_embed.py`)[cite: 5, 13].
* **Interactive Command Console**: Material risk matrix tracking for Automotive Bill of Materials (BOM) alongside live operational KPI alert cards[cite: 5, 13].
* **Enterprise Security & Auth**: Azure AD OAuth service principal token management and HashiCorp Vault access policy enforcement[cite: 8, 13].

---

##  System Screenshots & Interface Preview

<div align="center">

###  Executive Control Tower Dashboard & Power BI Embed
*Real-time supply chain telematics, BOM risk matrix, and embedded Power BI workspace report.*

![Executive Control Tower Dashboard](docs/Screenshot/control_tower.png)

<br/>

###  Agentic_Risk_Assessment
*LangGraph state machine routing requests across Researcher, Risk Analyst, and Critic node.*

![Agentic Risk Assessment and Precautionary Measures](docs/Screenshot/Agentic_risk_assessment.png)

<br/>

###  Control and Risk Metrics
*Stock Risk association and control .*

![Risk_Metrics](docs/Screenshot/Critical_sock_risk_metric.png)

</div>

---

---

##  Architecture & Data Pipeline

```text
[ Real-Time Telematics / Kafka Producer ]
                  │
                  ▼ (JSON Telemetry Events over Port 9092)
        [ Apache Kafka Broker ]
                  │
                  ▼ (Topic: telemetry_topic)
  [ PySpark Structured Streaming Pipeline ]
    ├── Schema Enforcement & Cleaning
    └── Thermal / Speed Anomaly Enrichment
                  │
                  ▼ (Micro-batch Upserts via PostgreSQL JDBC)
   [ PostgreSQL Operational Store (control_tower_db) ]
    ├── telemetry_events
    ├── warehouse_facilities
    ├── fulfillment_kpis
    └── inventory_stock
                  │
        ┌─────────┴────────────────────────┐
        ▼                                  ▼
[ Streamlit UI + Power BI Embed ]    [ LangGraph Multi-Agent Engine ]
  ├── Power BI Interactive Reports     ├── Researcher Node
  ├── Real-time Telemetry Stream       ├── Risk Analyst Node
  └── HITL Command Console             └── Critic Verification Node
```
---

##  Technology Stack

| Component | Technology / Library |
| :--- | :--- |
| **Messaging Queue** | Apache Kafka |
| **Stream Engine** | Apache Spark Structured Streaming (PySpark 3.5.0) |
| **Operational Database** | PostgreSQL 16 (`control_tower_db`) |
| **Agentic AI Engine** | LangGraph, LangChain, Groq (Llama-3.3-70B) / AWS Bedrock |
| **User Interface** | Streamlit, Streamlit Components v1, Plotly Express |
| **Business Intelligence** | Power BI Desktop & Power BI Service Embedded iFrame |
| **Database Drivers** | PostgreSQL JDBC Driver (`postgresql-42.6.0.jar`), Spark Kafka Connector (`spark-sql-kafka-0-10_2.12`) |

---

## Complete Repository Architecture & File Directory

```text
stern-watch-control-tower/
├── .github/
│   └── workflows/
│       ├── ci.yml                # Automated pytest E2E testing & security scanning pipeline
│       └── secret_scan.yml       # Automated GitHub Push Protection & credential leak checks
├── config/
│   ├── __init__.py               # Package initialization marker
│   ├── logging_config.json       # Structured JSON logger handlers & log levels
│   ├── powerbi_config.json       # Power BI embed specs, report IDs, & tenant mappings
│   ├── security_policy.yaml      # HMAC signature validation rules & HITL permission matrices
│   └── settings.py               # Centralized connection URIs, environment variables, & secret bindings
├── data/
│   ├── mocks/                    # Mock supplier feeds & BOM inventory status datasets
│   ├── sample_manifests/         # Sample shipping manifests & customs documentation
│   └── telemetry_fixtures/       # Real-time GPS & thermal sensor test payloads
├── deployment/
│   ├── docker/
│   │   ├── Dockerfile.airflow    # Orchestration service container image
│   │   ├── Dockerfile.spark      # PySpark Structured Streaming consumer image
│   │   └── Dockerfile.streamlit  # Control tower web application container image
│   ├── helm/stern-watch/
│   │   ├── templates/            # Kubernetes resource manifests (Deployments, Services, Ingress)
│   │   ├── Chart.yaml            # Helm chart metadata & version control
│   │   └── values.yaml           # Environment-specific values (replica counts, ports, memory limits)
│   ├── terraform/
│   │   ├── modules/              # Reusable IaC infrastructure modules (EKS, RDS, MSK)
│   │   ├── main.tf               # Primary Terraform provider & resource definitions
│   │   └── variables.tf          # Configurable infrastructure variables & secrets schema
│   └── docker-compose.yml        # Multi-container orchestration (PostgreSQL, Kafka, Streamlit)
├── docs/
│   ├── architecture/
│   │   ├── control_tower_architecture.png  # High-level enterprise control tower schematic
│   │   ├── data_flow_diagram.png            # End-to-end Kafka & Spark telemetry streaming flow
│   │   └── multi_agent_cyclical_flow.png   # Cyclical LangGraph multi-agent interaction graph
│   ├── security/
│   │   ├── data_governance_framework.md     # Governance, metadata, & lineage tracking specification
│   │   └── rbac_matrix.md                  # Role-Based Access Control permission matrix
│   └── deployment_guide.md                  # Comprehensive platform deployment manual
├── mlops/
│   ├── data_validation/
│   │   └── expectations/
│   │       ├── manifests_suite.json         # Great Expectations validation suite for shipping manifests
│   │       └── telemetry_suite.json         # Great Expectations validation suite for Kafka telemetry
│   ├── drift_monitors/
│   │   └── ks_test_drift.py                 # Kolmogorov-Smirnov statistical data drift monitoring script
│   └── mlflow_config.yaml                   # MLflow experiment tracking & model registry configuration
├── orchestration/
│   ├── dags/
│   │   ├── __init__.py                   # DAG package marker
│   │   ├── dag_batch_lakehouse_etl.py    # Airflow DAG for Lakehouse batch ingestion
│   │   ├── dag_graph_sync.py             # Airflow DAG for LangGraph state sync
│   │   ├── dag_ml_retrain_drift_check.py # Airflow DAG for drift monitoring & retraining
│   │   └── dag_powerbi_dataset_refresh.py# Airflow DAG triggering Power BI dataset refresh
│   ├── plugins/
│   │   ├── __init__.py                   # Airflow plugins package marker
│   │   └── custom_operators.py           # Custom Airflow hooks and operators
│   └── __init__.py                       # Orchestration package initialization
├── security/
│   ├── hitl_audit/
│   │   └── approval_logger.py            # Audit logger for Human-In-The-Loop operator sign-offs
│   ├── kms/
│   │   └── key_rotation_policy.json      # AWS KMS secret key rotation policy definition
│   ├── neo4j_rbac/
│   │   └── cypher_security_rules.cypher  # Cypher graph access control policies
│   └── vault/
│       └── policy.hcl                    # HashiCorp Vault access policy definition
├── src/
│   ├── agents/
│   │   ├── tools/
│   │   │   ├── __init__.py       # Agent tools package marker
│   │   │   ├── neo4j_tools.py    # Knowledge graph & lineage query tools
│   │   │   ├── pgvector_tools.py # Vector similarity search & RAG retrieval tools
│   │   │   └── sap_bapi_tools.py # SAP ERP integration & BAPI execution functions
│   │   ├── __init__.py           # Agents package marker
│   │   ├── critic.py             # Critic Agent node verifying factual accuracy & guardrails
│   │   ├── graph_builder.py      # LangGraph state machine compiler & edge routing logic
│   │   ├── researcher.py         # Researcher Agent node querying inventory context
│   │   ├── risk_analyst.py       # Risk Analyst node calculating line-stoppage financial costs
│   │   └── state.py              # AgentState TypedDict (research, analysis, critic feedback)
│   ├── common/
│   │   ├── __init__.py           # Common package initialization marker
│   │   ├── db_clients.py         # Database connection poolers (PostgreSQL, Neo4j, ChromaDB)
│   │   ├── exceptions.py         # Custom application exception handlers & error schemas
│   │   ├── logger.py             # Global logging instance wrapper
│   │   └── security.py           # Core cryptographic token generation & security utils
│   ├── ingestion/
│   │   ├── batch_etl/
│   │   │   ├── __init__.py       # Batch ETL package marker
│   │   │   ├── neo4j_graph_sync.py# Graph synchronization job for Neo4j supply chain nodes
│   │   │   └── sap_idoc_extractor.py # Extractor module for SAP IDoc data documents
│   │   ├── kafka_producers/
│   │   │   ├── __init__.py       # Kafka producers package marker
│   │   │   ├── erp_cdc_producer.py# Change Data Capture (CDC) producer for ERP updates
│   │   │   └── telemetry_producer.py # Streams vehicle speed, location, & thermal JSON
│   │   ├── spark_streaming/
│   │   │   ├── __init__.py       # Spark streaming package marker
│   │   │   ├── customs_manifest_parser.py # PySpark parser for shipping manifests & customs data
│   │   │   └── telemetry_geofence_stream.py # PySpark consumer writing micro-batches to Postgres
│   │   └── __init__.py           # Ingestion package initialization
│   ├── models/
│   │   ├── delay_predictor/
│   │   │   ├── __init__.py       # Delay predictor package marker
│   │   │   ├── feature_engineering.py # Feature extraction for shipment & ETA delays
│   │   │   ├── predict.py        # Inference endpoint for transit delay predictions
│   │   │   └── train.py          # Training pipeline for transit delay ML models
│   │   ├── demand_forecaster/
│   │   │   ├── __init__.py       # Demand forecaster package marker
│   │   │   ├── inventory_runout_eval.py # Inventory depletion & safety stock runout evaluator
│   │   │   └── prophet_forecaster.py # Time-series Prophet forecasting for material demand
│   │   └── __init__.py           # Models package initialization
│   ├── powerbi/
│   │   ├── __init__.py           # Power BI integration package marker
│   │   ├── auth.py               # Azure AD service principal OAuth token manager
│   │   └── push_api_client.py    # Power BI REST Push API client for dataset updates
│   ├── ui/
│   │   ├── assets/
│   │   │   ├── mercedes_logo.svg # Mercedes-Benz branding asset for header
│   │   │   └── styles.css        # Custom CSS rules for Streamlit layout styling
│   │   ├── components/
│   │   │   ├── __init__.py       # UI components package marker
│   │   │   ├── agent_console.py  # Interactive multi-agent command & control console
│   │   │   ├── bom_table.py      # Automotive BOM material risk matrix & supplier tracker
│   │   │   ├── header.py         # Navigation header & live telemetry indicator component
│   │   │   ├── kpi_cards.py       # Metric summary cards for operational risk & ETA alerts
│   │   │   └── powerbi_embed.py  # Embedded interactive Power BI dashboard iFrame tab
│   │   ├── __init__.py           # UI package marker
│   │   └── main.py               # Primary Streamlit application entry point
│   └── __init__.py               # Source root package initialization
├── tests/
│   ├── e2e/
│   │   └── test_streamlit_workflow.py# Playwright/Selenium E2E workflow testing for UI dashboard
│   ├── integration/
│   │   ├── test_kafka_pipeline.py# Integration test for Kafka producers and Spark consumers
│   │   └── test_neo4j_queries.py # Integration test for Neo4j supply chain graph queries
│   ├── unit/
│   │   ├── test_agents.py        # Unit tests for LangGraph Researcher, Analyst, and Critic
│   │   ├── test_powerbi_auth.py  # Unit test for Azure AD OAuth token generation
│   │   ├── test_security.py      # Unit test for cryptographic signatures & RBAC validation
│   │   └── test_spark_etl.py     # Unit test for PySpark schema transformations
│   └── conftest.py               # Global Pytest fixtures, mock DB drivers, & environment setups
├── .dockerignore                 # Excluded paths for Docker container builds
├── .env.example                  # Sanitized environment variable configuration template
├── .gitignore                    # Git tracking exclusion rules (excludes .env & secrets)
├── LICENSE                       # Open-source license terms
├── Makefile                      # Automated setup, database initialization, and run commands
├── pyproject.toml                # Project build system, tool configs, and ruff/black settings
├── README.md                     # Executive platform documentation & architecture guide
├── requirements.txt              # Core Python dependency manifest
└── setup.cfg                     # Legacy package metadata & flake8 linter rules
```
---

##  Prerequisites & Setup

### Prerequisites
1. **Python 3.10+**
2. **JDK 17+** (Required for PySpark execution)
3. **PostgreSQL 16** running locally on port `5432`
4. **Apache Kafka** running locally on port `9092`

### 1. Environment Setup
Clone the repository and create a virtual environment:
```bash
git clone [https://github.com/your-username/stern-watch-control-tower.git](https://github.com/your-username/stern-watch-control-tower.git)
cd stern-watch-control-tower

python -c "import venv" || python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
2. Configure Database SchemaCreate the control_tower_db database in PostgreSQL and initialize all operational tables:Bashmake db-init
Running the PlatformYou can manage all processes individually or concurrently using the provided Makefile.Start Kafka Telemetry Producer:Bashmake run-producer
Start PySpark Streaming Consumer:Bashmake run-spark
Launch Streamlit Control Tower UI:Bashmake run-ui
Power BI Embedding SetupOpen control_tower_report.pbix inside Power BI Desktop.Connect to your local PostgreSQL database (control_tower_db).Set the table storage mode to Import.Click Publish to publish the report to your Power BI Workspace (app.powerbi.com).In Power BI Service, go to File $\rightarrow$ Embed report $\rightarrow$ Website or portal (or Publish to Web).Copy the "Link to embed this content" URL and paste it into POWERBI_EMBED_URL inside src/ui/components/powerbi_embed.py.
