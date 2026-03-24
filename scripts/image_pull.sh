#!/usr/bin/env bash
set -euo pipefail

images=(
  "docker.io/apache/airflow:2.11.2"
  "docker.io/prometheuscommunity/postgres-exporter:v0.19.1"
  "docker.io/prom/statsd-exporter:v0.28.0"
  "docker.io/prom/prometheus:v3.10.0"
  "docker.io/grafana/grafana:12.4.1"
  "docker.io/library/busybox:1.37.0"
  "docker.io/jenkins/jenkins:2.541.3-lts-jdk21"
  "docker.io/library/postgres:14.22-trixie"
)

for image in "${images[@]}"; do
  echo "Pulling $image ..."
  sudo crictl pull "$image"
done

echo
echo "Pulled images:"
sudo crictl images | egrep 'airflow|postgres-exporter|statsd-exporter|prometheus|grafana|busybox|jenkins|postgres'