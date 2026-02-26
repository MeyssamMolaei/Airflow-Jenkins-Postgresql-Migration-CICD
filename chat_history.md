# Chat History - Airflow-Jenkins-Postgresql-Migration-CICD

## Project Overview
**Objective**: Create an automated data migration pipeline between two Postgresql instances (P1 to P2) using Airflow for orchestration, Jenkins for task triggering, and GitHub Actions for CI/CD deployment to a Kubernetes cluster on a remote Ubuntu 24 server (`home.meyssam.ir`).

## Conversation Summary

### 1. Initial Request
The user requested a full training setup for:
- Two Postgres instances (P1 contains data, P2 is the target).
- Airflow (Standalone image) to handle data sync.
- Jenkins to create tasks for Airflow.
- Deployment via GitHub Actions (SSH/SCP) to an Ubuntu 24 host (dual core, 4GB RAM) with an existing Kubernetes service.

### 2. Implementation Strategy
We planned a modular approach using Kubernetes manifests and environment-driven configurations.

### 3. Accomplishments
1.  **Infrastructure Design**:
    *   Created `kubernetes/postgres-p1.yaml`: Deployment for source DB with an initialization script to populate sample data.
    *   Created `kubernetes/postgres-p2.yaml`: Deployment for the target DB.
    *   Created `kubernetes/airflow.yaml`: Standalone Airflow deployment using ConfigMaps for DAGs and pre-configured environment variables for database connections.
    *   Created `kubernetes/jenkins.yaml`: Jenkins deployment with setup wizard disabled for faster automation.

2.  **Orchestration Logic**:
    *   Created `airflow/dags/db_sync.py`: A Python-based Airflow DAG that connects to both Postgres instances, fetches data from P1, and performs a clean sync into P2.

3.  **Pipeline Automation**:
    *   Updated `Jenkinsfile`: Added a stage to trigger the Airflow sync DAG via the REST API using `curl`.
    *   Created `.github/workflows/deploy.yml`: A GitHub Action workflow that uses `appleboy/scp-action` and `appleboy/ssh-action` to push manifests and apply them to the remote server.

4.  **Documentation provided**:
    *   `implementation_plan.md`: A roadmap of the project.
    *   `setup_instructions.md`: Detailed steps for configuring GitHub Secrets and Jenkins Credentials.

## Key Configuration Details
- **Airflow Web UI**: Port 30080
- **Jenkins Web UI**: Port 30090
- **Postgres P1 Connection**: `postgresql://postgres:p1password@postgres-p1:5432/source_db`
- **Postgres P2 Connection**: `postgresql://postgres:p2password@postgres-p2:5432/target_db`

## Future Recommendations
- Configure PersistentVolumeClaims (PVCs) for Postgres and Airflow if data persistence across pod restarts is required.
- Implement incremental sync (using timestamps or IDs) instead of full refresh for larger datasets.
