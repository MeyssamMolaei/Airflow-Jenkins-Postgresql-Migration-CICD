import pandas as pd
from sqlalchemy import create_engine
# from airflow import DAG
# from airflow.providers.standard.operators.python import PythonOperator
# from datetime import datetime

# def analyze_db():
#     engine = create_engine("postgresql+psycopg2://postgres:p1password@postgres-p1:5432/source_db")
#     df = pd.read_sql('SELECT * FROM employees', engine)
#     print(df.head())

# with DAG(
#     dag_id='db_analyze',
#     start_date=datetime(2022, 1, 1),
#     schedule='@daily',
#     catchup=False
# ) as dag:
#     analyze_db_task = PythonOperator(
#         task_id='analyze_db',
#         python_callable=analyze_db,
#     )
engine = create_engine("postgresql+psycopg2://postgres:p1password@postgres-p1:5432/source_db")
query = "SELECT * FROM public.employees;"
df = pd.read_sql(query, engine)

print(df.head())
print(df.shape)
print(df.dtypes)