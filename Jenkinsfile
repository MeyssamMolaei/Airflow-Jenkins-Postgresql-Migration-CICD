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
                        curl -X POST "${AIRFLOW_URL}/api/v1/dags/${AIRFLOW_DAG_ID}/dagRuns" \
                        -H "Content-Type: application/json" \
                        --user "${AIRFLOW_CREDENTIALS}" \
                        -d '{}'
                    """
                }
            }
        }
    }
}
