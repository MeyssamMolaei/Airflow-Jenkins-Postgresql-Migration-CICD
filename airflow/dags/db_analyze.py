import pandas as pd
from sqlalchemy import create_engine
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def analyze_db():
    engine = create_engine("postgresql+psycopg2://postgres:p1password@postgres-p1:5432/source_db")
    df = pd.read_sql('SELECT * FROM employees limit 10', engine)
    print(df.head())

with DAG(
    dag_id='db_analyze',
    start_date=datetime(2022, 1, 1),
    schedule='@once',
    catchup=False
) as dag:
    analyze_db_task = PythonOperator(
        task_id='analyze_db',
        python_callable=analyze_db,
    )
