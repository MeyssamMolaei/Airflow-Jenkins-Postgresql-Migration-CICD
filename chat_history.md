# Chat History - Airflow-Jenkins-Postgresql-Migration-CICD

## Project Overview
**Objective**: Create an automated data migration pipeline between two Postgresql instances (P1 to P2) using Airflow for orchestration, Jenkins for task triggering, and GitHub Actions for CI/CD deployment to a Kubernetes cluster on a remote Ubuntu 24 server (`home.meyssam.ir`).

## 🛠️ Implementation Summary (Updated)

### 1. Infrastructure, Stability & Data Persistence
- **StatefulSets**: Converted all deployments across the board to `StatefulSet` so that **all pods have static names**:
    - `airflow-0`, `jenkins-0`, `postgres-p1-0`, `postgres-p2-0`, `grafana-0`.
    - `postgres-exporter-p1-0`, `postgres-exporter-p2-0`, `statsd-exporter-0`.
- **Persistent Storage (`hostPath`)**: Set up robust data retention mapped to local server directories (`/home/development/deployment/...`).
    - *Postgres P1/P2*: Mapped data nodes dynamically using `initContainers` fixing recursive `chown 999:999` permissions to resolve user write conflicts.
    - *Jenkins*: Protected Jenkins master configurations mapping to `/var/jenkins_home` (`chown 1000:1000`).
    - *Grafana*: Protected raw dashboard plugins and UI settings mapping strictly to `/var/lib/grafana` (`chown 472:472`).
- **Exposed Services**: 
    - **P1 Port**: 30433 (External) / 5432 (Internal)
    - **P2 Port**: 30434 (External) / 5432 (Internal)
    - **Grafana Port**: 30070 (External) / 3000 (Internal)

### 2. Monitoring & Observability Stack
- **Prometheus Pipeline**: Deployed `kubernetes/prometheus.yaml` to scrape system metrics rapidly. Set as a fully automated default Data Source in Grafana.
- **Exporters (`kubernetes/exporters.yaml`)**:
    - **Postgres Exporter P1/P2**: Running cleanly on port 9187 interacting with database endpoints directly.
    - **StatsD Exporter**: Capturing live metric hooks natively from Airflow execution nodes on UDP port 8125.
- **Airflow Initialization Order**: Attached an explicit `initContainer` running sequential `pg_isready` queries forcing Airflow to sleep 30 seconds explicitly *after* the databases boot, completely eliminating race conditions.

### 3. Airflow Configuration & Code Expansion
- **Airflow Tuning**: CPU Parsing fixed (`MIN_FILE_PROCESS_INTERVAL: 1`), Timezone locked to `Europe/Stockholm`, StatsD telemetry (`AIRFLOW__METRICS__STATSD_ON`) fully enabled.
- **DAG Enhancements (`db_sync.py`)**: 
    - Database schema significantly widened (`job_title`, `experience`, `age`, `education`, `city`, `tenure`, `skill_level`, and `created_at`).
    - Logic overhauled to leverage `psycopg2.extras.execute_values` for high-performance batch insertion resolving ON CONFLICT duplicates instantly.

### 4. CI/CD & Deployments
- **GitHub Actions**: Pipeline (`deploy.yml`) is completely destructive-first. Discards old Pods before triggering native rollout logic mirroring entire file blocks.
- **Data Generation Engine**: `scripts/generate_data.py` enhanced with over 50x naming parameters. Implemented a dynamic **5% Corrupted Data Injector** designed exclusively for data analysis exercises (negative salaries, non-existent cities, bizarre ages).

### 5. Jenkins Automation
- **API Token Handling**: `Jenkinsfile` rewritten to generate Airflow JWT tokens flawlessly using `cURL`, then explicitly commanding Airflow 2.x REST APIs to unpause synchronized tasks.

## 🔑 Crucial Connections
- **Postgres P1 (Internal)**: `postgresql://postgres:p1password@postgres-p1:5432/source_db`
- **Postgres P2 (Internal)**: `postgresql://postgres:p2password@postgres-p2:5432/target_db`
- **Airflow Web UI**: `http://home.meyssam.ir:30080` (User: `madmin`)
- **Grafana Web UI**: `http://home.meyssam.ir:30070` (User: `admin`, Pass: `admin123`)
- **Jenkins Web UI**: `http://home.meyssam.ir:30090`

## 📝 Recent Files Modified
- `kubernetes/exporters.yaml` & `prometheus.yaml`: Completely designed the scraping metrics structure.
- `kubernetes/postgres-*.yaml` & `kubernetes/jenkins.yaml` & `kubernetes/grafana.yaml`: Secured Data logic.
- `airflow/dags/db_sync.py`: DAG expanded for new columns (`created_at`).
- `scripts/generate_data.py`: Extended random generator values / dirty data logic.
