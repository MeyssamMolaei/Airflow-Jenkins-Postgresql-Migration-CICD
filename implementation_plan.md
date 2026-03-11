# Implementation Plan - Airflow-Jenkins-Postgresql-Migration-CICD

This project aims to demonstrate a complete CI/CD pipeline and data sync automation using Kubernetes, Postgres, Jenkins, and Airflow.

## 1. Infrastructure (Kubernetes)
Deploy the following components to the Ubuntu server (`home.meyssam.ir`):
- **Postgres P1 (Source)**: Contains original data.
- **Postgres P2 (Target)**: Destination for synced data.
- **Airflow**: Orchestrates the sync between P1 and P2.
- **Jenkins**: Triggers Airflow tasks relative to build/deployment events.

## 2. CI/CD Pipeline (GitHub Actions)
- On push to `main`, GitHub Actions will:
    1. SSH into the Ubuntu server.
    2. Apply Kubernetes manifests to update the deployment.

## 3. Automation Logic (Airflow & Jenkins)
- **Airflow**: A Python DAG will connect to P1 and P2, refreshing data in P2.
- **Jenkins**: A Jenkinsfile will include a stage to trigger the Airflow DAG via API.

## 4. Immediate Steps
- [x] Create K8s manifests for Postgres P1 & P2.
- [x] Create K8s manifests for Airflow (Standalone).
- [x] Create K8s manifests for Jenkins.
- [x] Create an Airflow DAG for DB sync.
- [x] Create a GitHub Action workflow for SSH deployment.
- [x] Update Jenkinsfile with trigger logic.
