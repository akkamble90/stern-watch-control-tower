# Enterprise Data Governance & Cryptographic Framework

## 1. Data Encryption Standards
* **Encryption at Rest:** All PostgreSQL data blocks, Neo4j volume mounts, and Delta Lakehouse storage are encrypted using **AES-256-GCM**.
* **Encryption in Transit:** Communications across Kafka topics, PySpark worker nodes, database sockets, and Web browsers enforce **TLS 1.3**.

## 2. Human-In-The-Loop (HITL) Immutable Audit Log
All financial orders, supplier re-routings, or manual agent overrides executed through the Control Tower frontend create a cryptographically signed audit log stored in PostgreSQL:

$$\text{Audit\_Signature} = \text{HMAC-SHA256}\left(\text{Secret\_Key}, \text{Timestamp} \parallel \text{UserID} \parallel \text{ActionPayload}\right)$$

This ensures that no operator can retroactively alter or dispute operational approval logs.

## 3. Secret Management
Zero plaintext credentials are stored in Git repositories. Production secrets are managed via HashiCorp Vault / External Secrets Operator and mounted dynamically into Kubernetes pods at runtime.