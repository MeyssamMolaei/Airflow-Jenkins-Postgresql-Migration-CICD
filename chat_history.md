# Chat History - Airflow-Jenkins-Postgresql-Migration-CICD

## Project Overview
**Objective**: Create an automated data migration pipeline between two Postgresql instances (P1 to P2) using Airflow for orchestration, Jenkins for task triggering, and GitHub Actions for CI/CD deployment to a Kubernetes cluster on a remote Ubuntu 24 server (`home.meyssam.ir`).

## 🛠️ Implementation Summary (Updated)

### 1. Infrastructure & Stability
- **StatefulSets**: Converted all deployments (Airflow, Jenkins, Postgres P1, Postgres P2, Grafana) to `StatefulSet`.
    - **Stable Pod Names**: `airflow-0`, `jenkins-0`, `postgres-p1-0`, `postgres-p2-0`, `grafana-0`.
- **Exposed Services**: Services are exposed via NodePort.
    - **P1 Port**: 30433 (External) / 5432 (Internal)
    - **P2 Port**: 30434 (External) / 5432 (Internal)
    - **Grafana Port**: 30070 (External) / 3000 (Internal)
- **HostPaths**: Airflow DAGs and Grafana Dashboards are loaded directly from the host server.
    - Airflow DAGs: `/home/development/deployment/airflow/dags`
    - Grafana Dashboards: `/home/development/deployment/grafana/dashboards` (Using `DirectoryOrCreate` to prevent `ContainerCreating` hangs).

### 2. Monitoring & Observability
- **DataDog**: Added `kubernetes/datadog.yaml` to deploy a DataDog Agent that automatically monitors both Postgres instances. (Requires API key configuration).
- **Grafana**: Deployed Grafana with pre-configured Data Sources connecting flawlessly to `Postgres-P1` and `Postgres-P2`. It mounts dashboard configurations automatically.

### 3. Airflow Configuration & Optimization
- **Credentials**: Fixed admin account created via custom entrypoint (`madmin`).
- **Timezone**: Set default timezone to `Europe/Stockholm`.
- **CPU Optimization**: Reduced DAG parsing frequency (`MIN_FILE_PROCESS_INTERVAL: 1`), configured resource limits, and capped active tasks.
- **DAG Optimization (`db_sync.py`)**: 
    - Re-wrote `db_sync.py` to use `psycopg2.extras.execute_values` for high-performance batch insertion.
    - Added sync support for the `created_at` timestamp.
    - Handles conflicts smoothly with `ON CONFLICT (id) DO UPDATE SET`.

### 4. CI/CD & Deployments
- **GitHub Actions**: `.github/workflows/deploy.yml` utilizes SCP to deploy `kubernetes/`, `scripts/`, `airflow/dags/`, and `grafana/` directories.
- **Cleanup**: Implemented `kubectl delete ...` to discard old pods cleanly before new applies roll out.
- **Data Generation**: `scripts/generate_data.py` enhanced with a rich, expansive list of first/last names to populate realistic mock sets over 100,000s of lines.

### 5. Jenkins Automation
- **API Token Handling**: `Jenkinsfile` rewritten to properly generate Airflow JWT tokens and interact with Airflow 2.x API using the `PATCH` endpoint to unpause jobs dynamically.

## 🔑 Crucial Connections
- **Postgres P1 (Internal)**: `postgresql://postgres@postgres-p1:5432/source_db`
- **Postgres P2 (Internal)**: `postgresql://postgres@postgres-p2:5432/target_db`
- **Airflow Web UI**: `http://home.meyssam.ir:30080` (User: `madmin`)
- **Grafana Web UI**: `http://home.meyssam.ir:30070` (User: `admin`, Pass: `admin123`)
- **Jenkins Web UI**: `http://home.meyssam.ir:30090`

## 📝 Recent Files Modified
- `kubernetes/grafana.yaml`: Grafana deployment and fixing `hostPath` Volume setup.
- `kubernetes/datadog.yaml`: DataDog configurations setup.
- `airflow/dags/db_sync.py`: DAG expanded for new columns (`created_at`).
- `scripts/generate_data.py`: Extended random generator values.
- `Jenkinsfile`: Refactored to properly communicate via Airflow REST API.
