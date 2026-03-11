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



// curl -sS -X POST 'http://192.168.1.88:30080/auth/token'   -H 'Content-Type: application/json'   -d '{"   -H 'Content-Type: application/json'   -d '{"username": "admin", "password": ""}'



//  curl -sS -X POST 'http://192.168.1.88:30080/api/v2/dags/postgres_sync_p1_to_p2/dagRuns'   -H "Authorization: Bearer $TOKEN"   -H 'Content-Type: application/json'   -d "{\"logical_date\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"dag_run_id\":\"jenkins_$(date +%s)\",\"conf\":{\"source\":\"jenkins\"}}"


// {"dag_run_id":"jenkins_1772667331","dag_id":"postgres_sync_p1_to_p2","logical_date":"2026-03-04T23:35:31Z","queued_at":"2026-03-04T23:35:31.853984Z","start_date":null,"end_date":null,"duration":null,"data_interval_start":"2026-03-04T23:35:31Z","data_interval_end":"2026-03-04T23:35:31Z","run_after":"2026-03-04T23:35:31.849207Z","last_scheduling_decision":null,"run_type":"manual","state":"queued","triggered_by":"rest_api","triggering_user_name":"Anonymous","conf":{"source":"jenkins"},"note":null,"dag_versions":[{"id":"019cbb1f-eb4e-7487-a93d-55e699bd345d","version_number":1,"dag_id":"postgres_sync_p1_to_p2","bundle_name":"dags-folder","bundle_version":null,"created_at":"2026-03-04T23:12:37.198613Z","dag_display_name":"postgres_sync_p1_to_p2","bundle_url":null}],"bundle_version":null,"dag_display_name":"postgres_sync_p1_to_p2"}