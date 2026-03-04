# Chat History - Airflow-Jenkins-Postgresql-Migration-CICD

## Project Overview
**Objective**: Create an automated data migration pipeline between two Postgresql instances (P1 to P2) using Airflow for orchestration, Jenkins for task triggering, and GitHub Actions for CI/CD deployment to a Kubernetes cluster on a remote Ubuntu 24 server (`home.meyssam.ir`).

## 🛠️ Implementation Summary (Updated)

### 1. Infrastructure & Stability
- **StatefulSets**: Converted all deployments (Airflow, Jenkins, Postgres P1, Postgres P2) to `StatefulSet`.
    - **Stable Pod Names**: `airflow-0`, `jenkins-0`, `postgres-p1-0`, `postgres-p2-0`.
- **Exposed Services**: Postgres instances are exposed via NodePort.
    - **P1 Port**: 30433 (External) / 5432 (Internal)
    - **P2 Port**: 30434 (External) / 5432 (Internal)
- **Airflow DAGs**: Switched from ConfigMap volumes to `hostPath`. DAGs are now deployed to `/home/development/deployment/airflow/dags` on the host server.

### 2. Airflow Configuration & Optimization
- **Credentials**: Fixed admin account created via custom entrypoint:
    - **User**: `madmin`
    - **Password**: `!!Anaconda@1981##`
- **CPU Optimization**:
    - Reduced DAG parsing frequency to 30s.
    - Set resource limits to cap Airflow at 1 CPU core (250m request, 1000m limit).
    - Capped parallelism and active tasks.
- **DAG Optimization**: 
    - Re-wrote `db_sync.py` to use `execute_values` (batch insertion) instead of row-by-row loops. This allows efficient syncing of 100,000+ records with minimal CPU overhead.

### 3. CI/CD & Scripts
- **GitHub Actions**: Updated `.github/workflows/deploy.yml` with:
    - Cleanup step (`kubectl delete ... --all`) to ensure fresh deployments.
    - Deployment of `scripts/` and `airflow/dags/` folders via SCP.
    - Fixed `kubectl` flags for insecure TLS and validation skip.
- **Data Generation**: Created `scripts/generate_data.py` to populate P1 with random data via either internal ClusterIP or external NodePort.

### 4. Recent Infrastructure Updates
- **Server Setup Automation**: Created `scripts/setup_server.sh` to automate the installation of Python, K3s, and K9s on fresh Ubuntu 24.04 nodes.
- **User Migration**: Migrated the entire deployment from the `deploy` user to the `development` user, including SSH configurations and `hostPath` volume paths.
- **Postgres Authentication**: Disabled authentication for `postgres-p1` and `postgres-p2` using `POSTGRES_HOST_AUTH_METHOD: trust` to simplify internal communication and fix connection issues.
- **Airflow Stability**:
    - Configured resource requests/limits (500m-1000m CPU, 1Gi-2Gi RAM).
    - Optimized scheduler intervals (`MIN_FILE_PROCESS_INTERVAL: 30`) to reduce CPU overhead.
    - Updated connection strings to passwordless format.
- **Diagnostics**: Created `scripts/debug_k8s.sh` to collect pod logs and analyze cluster events for troubleshooting.

## 🔑 Crucial Connections
- **Postgres P1 (Internal)**: `postgresql://postgres@postgres-p1:5432/source_db` (Trust Auth)
- **Postgres P2 (Internal)**: `postgresql://postgres@postgres-p2:5432/target_db` (Trust Auth)
- **Airflow Web UI**: `http://home.meyssam.ir:30080` (User: `madmin`)
- **Jenkins Web UI**: `http://home.meyssam.ir:30090`

## 📝 Recent Files Modified
- `kubernetes/airflow.yaml`: Resource tuning and passwordless connections.
- `kubernetes/postgres-p1.yaml` & `postgres-p2.yaml`: Enabled `trust` authentication.
- `.github/workflows/deploy.yml`: Switched to `development` user and added setup/debug support.
- `scripts/debug_k8s.sh`: New diagnostic tool.
- `scripts/setup_server.sh`: New server initialization script.
