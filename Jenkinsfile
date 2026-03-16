pipeline {
    agent any

    environment {
        AIRFLOW_URL = "http://airflow:8080"
        AIRFLOW_DAG_ID = "postgres_sync_p1_to_p2"
        // These should be configured as credentials in Jenkins
        AIRFLOW_CREDENTIALS = credentials('airflow-api-auth')
    }

    stages {
        stage('Hello Jenkins') {
            steps {
                sh 'echo "Jenkins is starting the migration pipeline 🚀"'
            }
        }

        stage('Trigger Airflow Sync') {
            steps {
                script {
                    sh """
                        curl -X POST "${AIRFLOW_URL}/api/v2/dags/${AIRFLOW_DAG_ID}/dagRuns" \
                        -H "Content-Type: application/json" \
                        --user "${AIRFLOW_CREDENTIALS}" \
                        -d '{}'
                    """
                }
            }
        }
    }
}



// TOKEN="$(curl -sS -X POST 'http://192.168.1.88:30080/auth/token' \
//   -H 'Content-Type: application/json' \
//   -d '{"username":"admin","password":""}' \
//   | sed -n 's/.*"access_token":"\([^"]*\)".*/\1/p')"

// [ -n "$TOKEN" ] || { echo "Failed to get token"; exit 1; }

// curl -f -sS -X PATCH 'http://192.168.1.88:30080/api/v2/dags/postgres_sync_p1_to_p2' \
//   -H "Authorization: Bearer $TOKEN" \
//   -H 'Content-Type: application/json' \
//   -d '{"is_paused":false}'