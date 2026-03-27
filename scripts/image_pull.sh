#!/usr/bin/env bash
set -euo pipefail

images=(
  "docker.io/apache/airflow:latest"
  "docker.io/prometheuscommunity/postgres-exporter:latest"
  "docker.io/prom/statsd-exporter:latest"
  "docker.io/prom/prometheus:latest"
  "docker.io/grafana/grafana:latest"
  "docker.io/library/busybox:latest"
  "docker.io/jenkins/jenkins:latest"
  "docker.io/library/postgres:latest"
  "docker.io/library/mongo:latest"
)

for image in "${images[@]}"; do
  echo "Pulling $image ..."
  sudo ctr -n k8s.io images pull "$image"
done

echo
echo "Pulled images:"
sudo ctr -n k8s.io images list | egrep 'airflow|postgres-exporter|statsd-exporter|prometheus|grafana|busybox|jenkins|postgres|mongo'