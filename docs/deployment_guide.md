# PROJECT STERN-WATCH: ENTERPRISE DEPLOYMENT GUIDE

This document details the step-by-step procedures for deploying the Intelligent Supply Chain Control Tower across Local Development, Docker Compose, and Enterprise Kubernetes environments.

---

## 1. Local Development Setup (Quickstart)

### Prerequisites
* **OS:** Windows 11 / Linux (Ubuntu 22.04+) / macOS
* **Runtimes:** Python 3.11+, PowerShell 7+, Docker Desktop (v24.0+)
* **API Keys:** Groq API Key, Tavily Search Key, Azure AD / Power BI Credentials

### Installation
1. Clone the repository and navigate to the project root:
   ```bash
   git clone [https://github.com/your-org/stern-watch-control-tower.git](https://github.com/your-org/stern-watch-control-tower.git)
   cd stern-watch-control-tower