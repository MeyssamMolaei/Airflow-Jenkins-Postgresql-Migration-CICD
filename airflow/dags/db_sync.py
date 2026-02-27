from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

def sync_data():
    # Source (P1) connection
    src_hook = PostgresHook(postgres_conn_id='postgres_p1')
    src_conn = src_hook.get_conn()
    src_cursor = src_conn.cursor()

    # Target (P2) connection
    dest_hook = PostgresHook(postgres_conn_id='postgres_p2')
    dest_conn = dest_hook.get_conn()
    dest_cursor = dest_conn.cursor()

    # Get data from P1
    src_cursor.execute("SELECT id, name, department, salary FROM employees")
    rows = src_cursor.fetchall()

    # Create table in P2 if it doesn't exist
    dest_cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            department VARCHAR(100),
            salary NUMERIC
        )
    """)
    
    # Simple sync: Delete all and re-insert
    # dest_cursor.execute("DELETE FROM employees")
    
    # Batch Insertion (Much faster and lower CPU)
    from psycopg2.extras import execute_values
    
    insert_query = """
        INSERT INTO employees (id, name, department, salary) 
        VALUES %s 
        ON CONFLICT (id) DO UPDATE SET 
        name=EXCLUDED.name, 
        department=EXCLUDED.department, 
        salary=EXCLUDED.salary
    """
    
    execute_values(dest_cursor, insert_query, rows)

    dest_conn.commit()
    
    src_cursor.close()
    src_conn.close()
    dest_cursor.close()
    dest_conn.close()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'postgres_sync_p1_to_p2',
    default_args=default_args,
    description='Sync employees table from P1 to P2',
    schedule=None,
    catchup=False,
) as dag:

    sync_task = PythonOperator(
        task_id='sync_employees',
        python_callable=sync_data,
    )
