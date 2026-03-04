#!/bin/bash

# Diagnostic Script to find root cause of crashing Kubernetes pods
# Run this on the server as the development user

export KUBECONFIG=/home/development/.kube/config

echo "==========================================="
echo "🔍 K8s Diagnostic Report - $(date)"
echo "==========================================="

echo -e "\n[1] Pod Status Summary"
kubectl get pods -o wide

echo -e "\n[2] Checking for Crashing Pods (CrashLoopBackOff / Error)"
CRASHING_PODS=$(kubectl get pods | grep -E 'CrashLoopBackOff|Error|Pending' | awk '{print $1}')

if [ -z "$CRASHING_PODS" ]; then
    echo "✅ No pods in Error or CrashLoopBackOff state."
else
    for POD in $CRASHING_PODS; do
        echo "-------------------------------------------"
        echo "❌ Analyzing Pod: $POD"
        
        echo "--- Describe (Events) ---"
        kubectl describe pod $POD | grep -A 20 "Events:"
        
        echo "--- Recent Logs (Last 50 lines) ---"
        kubectl logs $POD --tail=50 || echo "Could not retrieve logs for $POD (perhaps it never started)"
        
        echo "--- Previous Container Logs (If crashed) ---"
        kubectl logs $POD -p --tail=50 2>/dev/null || echo "No previous container logs available."
    done
fi

echo -e "\n[3] System Resource Pressure"
echo "--- RAM Usage ---"
free -h
echo "--- Disk Space (If 100%, pods will crash) ---"
df -h /

echo -e "\n[4] Node Events (General Cluster Health)"
kubectl get events --sort-by='.lastTimestamp' | tail -n 15

echo "==========================================="
echo "✅ Diagnostic Done."
