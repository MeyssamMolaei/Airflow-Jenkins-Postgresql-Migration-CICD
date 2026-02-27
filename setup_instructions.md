# Setup Instructions

To get this automation running, follow these steps:

## 1. GitHub Secrets
In your GitHub repository, go to **Settings > Secrets and variables > Actions** and add the following:
- `SSH_KEY`: Your private SSH key to access `home.meyssam.ir`. (Used in GitHub Actions)
- `SSH_USERNAME`: Your SSH username (e.g., `root` or `meyssam`).

## 2. Jenkins Credentials
Once Jenkins is up at `http://home.meyssam.ir:30090`:
1.  Log in (retrieve the initial password if needed via `kubectl logs`).
2.  Go to **Manage Jenkins > Credentials > System > Global credentials**.
3.  Add a **Username with password** credential:
    - **ID**: `airflow-api-auth`
    - **Username**: `admin` (default Airflow admin)
    - **Password**: The password generated for Airflow standalone.

## 3. Airflow Connection Setup
The DAG expects connections named `postgres_p1` and `postgres_p2`. These are pre-configured via environment variables in `airflow.yaml`.

## 4. Bulk Data Generation (P1)
To test the migration, you need data in the source database. I've provided two ways to do this in the `scripts/` folder:

### Option A: Bash (Inside Server)
If you are logged into the Ubuntu host, run:
```bash
bash scripts/generate_data.sh
```
This uses `kubectl exec` to push data directly into the pod.

### Option B: Python (On Ubuntu Server)
To run the Python script directly on the server, you may need to install the dependencies first. Since the script now defaults to the service name `postgres-p1`, you can run it like this:

```bash
# Install dependencies if needed
sudo apt update && sudo apt install -y python3-pip
pip3 install psycopg2-binary

# Run the script (it will try to connect to 'postgres-p1')
# If the server is outside the K8s network, you may need to use the Service ClusterIP or NodeIP
python3 scripts/generate_data.py
```

## 5. Deployment
Simply push your changes to the `main` branch. GitHub Actions will handle:
1. Copying Kubernetes manifests, scripts, and **Airflow DAGs** to the server.
2. Applying the manifests.

> **Note**: Airflow now loads DAGs directly from the server's filesystem (`/home/deploy/deployment/airflow/dags`) using a `hostPath` volume. This makes it easier to add new DAGs without manual Kubernetes changes.
