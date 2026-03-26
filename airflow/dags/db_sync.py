from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
from psycopg2.extras import execute_values
import gc

BATCH_SIZE = 1000


def sync_data():
    src_hook = PostgresHook(postgres_conn_id='postgres_p1')
    dest_hook = PostgresHook(postgres_conn_id='postgres_p2')

    src_conn = src_hook.get_conn()
    dest_conn = dest_hook.get_conn()

    src_conn.autocommit = False
    dest_conn.autocommit = False

    total_rows = 0
    batch_no = 0

    try:
        with dest_conn.cursor() as dest_cursor:
            dest_cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(100),
                    department VARCHAR(100),
                    salary NUMERIC,
                    job_title VARCHAR(100),
                    experience INTEGER,
                    age INTEGER,
                    education VARCHAR(100),
                    city VARCHAR(100),
                    tenure NUMERIC,
                    skill_level VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            dest_conn.commit()

        insert_query = """
            INSERT INTO employees (
                id, name, department, salary, job_title,
                experience, age, education, city, tenure,
                skill_level, created_at
            )
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                department = EXCLUDED.department,
                salary = EXCLUDED.salary,
                job_title = EXCLUDED.job_title,
                experience = EXCLUDED.experience,
                age = EXCLUDED.age,
                education = EXCLUDED.education,
                city = EXCLUDED.city,
                tenure = EXCLUDED.tenure,
                skill_level = EXCLUDED.skill_level,
                created_at = EXCLUDED.created_at
        """

        # server-side cursor
        with src_conn.cursor(name="employees_sync_cursor") as src_cursor:
            src_cursor.itersize = BATCH_SIZE
            src_cursor.execute("""
                SELECT
                    id,
                    name,
                    department,
                    salary,
                    job_title,
                    experience,
                    age,
                    education,
                    city,
                    tenure,
                    skill_level,
                    created_at
                FROM public.employees
                where true
                and id is not null
                and name is not null
                and department is not null
                and salary > 0
                and job_title is not null
                and experience > 0
                and age > 0
                and education is not null
                and city is not null
                and tenure is not null
                and skill_level is not null
                and created_at is not null
                ORDER BY id
            """)

            while True:
                rows = src_cursor.fetchmany(BATCH_SIZE)
                if not rows:
                    break

                batch_no += 1

                with dest_conn.cursor() as dest_cursor:
                    execute_values(
                        dest_cursor,
                        insert_query,
                        rows,
                        page_size=BATCH_SIZE
                    )

                dest_conn.commit()

                total_rows += len(rows)
                print(f"Batch {batch_no}: synced {len(rows)} rows | total={total_rows}")

                # explicitly free memory
                del rows
                gc.collect()

    except Exception:
        dest_conn.rollback()
        raise

    finally:
        src_conn.close()
        dest_conn.close()


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='postgres_sync_p1_to_p2',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    description='Sync employees table from P1 to P2 in small batches',
    schedule='@once',
    catchup=False,
) as dag:

    sync_task = PythonOperator(
        task_id='sync_employees',
        python_callable=sync_data,
    )