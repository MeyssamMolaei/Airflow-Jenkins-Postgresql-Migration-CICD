from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pymongo
import gc

BATCH_SIZE = 1000

def sync_pg_to_mongo():
    # 1. Connect to Postgres (Source)
    pg_hook = PostgresHook(postgres_conn_id='postgres_p1')
    pg_conn = pg_hook.get_conn()
    
    # 2. Connect to MongoDB direct using pymongo authentication natively
    mongo_uri = "mongodb://admin:mongopassword@mongodb:27017/"
    mongo_client = pymongo.MongoClient(mongo_uri)
    mongo_db = mongo_client["migration_db"]
    mongo_collection = mongo_db["employees"]

    try:
        # Create an explicit unique native index mapped strictly back to Postgres IDs
        mongo_collection.create_index("id", unique=True)
        
        with pg_conn.cursor(name="pg_mongo_sync_cursor") as pg_cursor:
            pg_cursor.itersize = BATCH_SIZE
            pg_cursor.execute("""
                SELECT
                    id, name, department, salary, job_title,
                    experience, age, education, city, tenure,
                    skill_level, created_at
                FROM public.employees
                WHERE true
                AND id IS NOT NULL
                ORDER BY id
            """)

            batch_no = 0
            total_rows = 0

            while True:
                rows = pg_cursor.fetchmany(BATCH_SIZE)
                if not rows:
                    break
                
                batch_no += 1
                
                # Transform natively to dict documents for MongoDB execution mapped
                documents = []
                for row in rows:
                    doc = {
                        "id": row[0],
                        "name": row[1],
                        "department": row[2],
                        "salary": float(row[3]) if row[3] is not None else None,
                        "job_title": row[4],
                        "experience": row[5],
                        "age": row[6],
                        "education": row[7],
                        "city": row[8],
                        "tenure": float(row[9]) if row[9] is not None else None,
                        "skill_level": row[10],
                        "created_at": row[11]
                    }
                    documents.append(doc)

                # Execute secure asynchronous Multi-Query Bulk Upserts native to MongoDB engines
                from pymongo import UpdateOne
                operations = [
                    UpdateOne({"id": doc["id"]}, {"$set": doc}, upsert=True)
                    for doc in documents
                ]
                
                if operations:
                    mongo_collection.bulk_write(operations)

                total_rows += len(rows)
                print(f"Batch {batch_no}: synced {len(rows)} rows to MongoDB | total={total_rows}")

                # Safely flush the variables completely clearing ephemeral pipeline queues
                del rows
                del documents
                del operations
                gc.collect()

    except Exception as e:
        print(f"Error migrating to MongoDB: {e}")
        raise
    finally:
        pg_conn.close()
        mongo_client.close()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='postgres_to_mongo_migration',
    default_args=default_args,
    description='Sync employees table from Postgres P1 to MongoDB resiliently dynamically in batches',
    schedule='@once',
    catchup=False,
) as dag:

    sync_task = PythonOperator(
        task_id='sync_pg_to_mongo',
        python_callable=sync_pg_to_mongo,
    )
