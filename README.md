Markdown# Supply Chain Telemetry Control Tower & Agentic Command Center

An enterprise-grade, real-time supply chain monitoring platform and multi-agent AI risk engine. The system ingests high-frequency vehicle telemetry and warehouse inventory events via **Apache Kafka**, processes micro-batches with **PySpark Structured Streaming**, persists operational state to **PostgreSQL**, and renders an executive control tower in **Streamlit** embedded with **Power BI** interactive visual reports and a **LangGraph** multi-agent risk assessment command center.

---

##  Key Features

* **Real-time Event Ingestion & Streaming:** Ingests live vehicle telematics, GPS coordinates, ambient container temperatures, and speed telemetry using Apache Kafka.
* **Distributed Stream Processing:** High-throughput PySpark Structured Streaming consumer for schema enforcement, anomaly detection (thermal spike and congestion flags), and windowed database upserts.
* **Embedded Power BI Control Tower:** Embedded Power BI reports featuring stacked "water glass" warehouse storage capacity bars, pie charts for order fulfillment metrics (On-Time, Delayed, Returned), and interactive regional slicers.
* **Cyclic Multi-Agent AI System:** Built on **LangGraph** (Researcher $\rightarrow$ Risk Analyst $\rightarrow$ Critic) to dynamically evaluate line-halt financial exposures (€/day stoppage costs) and suggest automated freight rerouting strategies.
* **Automotive BOM Risk Tracking:** Strategic itemized monitoring across major vehicle subsystems (Engine/Powertrain, Braking, Suspension, Electrical, and Cooling/Exhaust).

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

##  Repository Structure

## 📂 Repository Structure

```text
stern-watch-control-tower/
├── config/
│   └── settings.py               # Centralized connection URIs and environmental variables
├── src/
│   ├── ingestion/
│   │   ├── kafka_producers/
│   │   │   └── telemetry_producer.py   # Simulates and streams vehicle telemetry JSON to Kafka
│   │   └── spark_streaming/
│   │       └── telemetry_geofence_stream.py # PySpark streaming consumer writing to PostgreSQL
│   ├── agents/
│   │   ├── state.py              # Shared AgentState TypedDict definition
│   │   ├── researcher.py         # Researcher Agent node extracting inventory context
│   │   ├── risk_analyst.py       # Risk Analyst node calculating line stoppage financial risks
│   │   ├── critic.py             # Critic Agent node enforcing quality & verifying factuality
│   │   └── graph_builder.py      # Compiles LangGraph state machine & edge routing
│   └── ui/
│       ├── main.py               # Primary Streamlit entry point
│       └── components/
│           ├── powerbi_embed.py  # Power BI iFrame embedded dashboard tab
│           ├── bom_table.py      # Material risk matrix & Automotive BOM tracking
│           └── agent_console.py  # Interactive multi-agent command console
├── Makefile                      # Automated setup, service execution, and build commands
├── requirements.txt              # Python dependency manifest
└── README.md                     # Technical documentation
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
