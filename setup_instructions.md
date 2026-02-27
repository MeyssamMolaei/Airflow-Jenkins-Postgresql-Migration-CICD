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
To run the Python script directly on the server, use either the Service Name or the Cluster IP. Note that when using the Cluster IP, you must use port **5432**.

```bash
# Using Service Name (Best)
python3 scripts/generate_data.py postgres-p1 5432

# Using Cluster IP (from kubectl get svc)
python3 scripts/generate_data.py 10.43.166.83 5432

# Using External/NodePort (from outside the cluster)
python3 scripts/generate_data.py home.meyssam.ir 30433
```

## 5. Deployment
Simply push your changes to the `main` branch. GitHub Actions will handle the Kubernetes deployment.
> **Note**: Deployment now uses `--insecure-skip-tls-verify=true` as per your updates.
