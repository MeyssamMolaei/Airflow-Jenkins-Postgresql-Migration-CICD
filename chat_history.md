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
- **Airflow DAGs**: Switched from ConfigMap volumes to `hostPath`. DAGs are now deployed to `/home/deploy/deployment/airflow/dags` on the host server.

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

## 🔑 Crucial Connections
- **Postgres P1 (Internal)**: `postgresql://postgres:p1password@postgres-p1:5432/source_db`
- **Postgres P2 (Internal)**: `postgresql://postgres:p2password@postgres-p2:5432/target_db`
- **Airflow Web UI**: `http://home.meyssam.ir:30080`
- **Jenkins Web UI**: `http://home.meyssam.ir:30090`

## 📝 Recent Files Modified
- `kubernetes/airflow.yaml`: StatefulSet, CPU optimizations, and user creation.
- `airflow/dags/db_sync.py`: Batch sync logic using `psycopg2.extras`.
- `.github/workflows/deploy.yml`: Cleanup and SCP folder sync.
- `scripts/generate_data.py`: Multipurpose data generation script.
