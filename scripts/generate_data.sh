#!/bin/bash
# Script to generate random data in Postgres P1 via kubectl exec

# Get the name of the Postgres P1 pod
POD_NAME=$(kubectl get pods -l app=postgres-p1 -o jsonpath="{.items[0].metadata.name}")

if [ -z "$POD_NAME" ]; then
    echo "❌ Error: Could not find postgres-p1 pod. Is the deployment running?"
    exit 1
fi

echo "🚀 Generating 100 random records in pod: $POD_NAME..."

# SQL to insert 100 random rows using generate_series
SQL_COMMAND=$(cat <<EOF
INSERT INTO employees (name, department, salary)
SELECT 
    'Emp_' || substring(md5(random()::text), 1, 8), 
    (ARRAY['Engineering', 'Product', 'Design', 'Marketing', 'Sales', 'HR', 'Finance'])[floor(random() * 7 + 1)],
    floor(random() * (150000 - 45000 + 1) + 45000)
FROM generate_series(1, 100) s(i);
EOF
)

# Execute the command inside the pod
kubectl exec -i $POD_NAME -- psql -U postgres -d source_db -c "$SQL_COMMAND"

if [ $? -eq 0 ]; then
    echo "✅ Success: 100 records generated in source_db (P1)."
    echo "📊 Current count in P1:"
    kubectl exec -i $POD_NAME -- psql -U postgres -d source_db -c "SELECT count(*) FROM employees;"
else
    echo "❌ Error: Failed to generate data."
fi
