# Setup Instructions

To get this automation running, follow these steps:

## 1. GitHub Secrets
In your GitHub repository, go to **Settings > Secrets and variables > Actions** and add the following:
- `SSH_PRIVATE_KEY`: Your private SSH key to access `home.meyssam.ir`.
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

## 4. Deployment
Simply push your changes to the `main` branch. GitHub Actions will handle the Kubernetes deployment to your Ubuntu server.
