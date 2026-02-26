import random
import string
import psycopg2 # Installation: pip install psycopg2-binary
import sys

def generate_random_name():
    first_names = ["John", "Jane", "Alex", "Emily", "Michael", "Sarah", "Chris", "Jessica", "David", "Laura"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def bulk_generate_p1_data(host="localhost", count=100):
    """
    Connects to Postgres P1 and inserts random employee data.
    Note: If running outside k8s, you must port-forward first:
    kubectl port-forward svc/postgres-p1 5432:5432
    """
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="p1password",  # As defined in postgres-p1.yaml
            host=host,
            port="5432",
            database="source_db"
        )
        cursor = connection.cursor()
        
        departments = ['Engineering', 'Product', 'Design', 'Marketing', 'Sales', 'HR', 'Finance']
        
        print(f"🔗 Connected to P1 at {host}. Inserting {count} records...")
        
        for i in range(count):
            name = generate_random_name()
            dept = random.choice(departments)
            salary = random.randint(45000, 160000)
            
            cursor.execute(
                "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)",
                (name, dept, salary)
            )
            
        connection.commit()
        print(f"✅ Successfully inserted {count} records into P1.")
        
        # Verify
        cursor.execute("SELECT count(*) FROM employees;")
        total = cursor.fetchone()[0]
        print(f"📊 Total records now in P1: {total}")
        
    except Exception as error:
        print(f"❌ Error: {error}")
        if "connection" in locals() and connection:
            connection.rollback()
    finally:
        if "connection" in locals() and connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # If running on the Ubuntu server, it can often resolve 'postgres-p1' via K8s DNS 
    # or you can pass the specific IP/Service Name as an argument.
    target_host = sys.argv[1] if len(sys.argv) > 1 else "postgres-p1"
    bulk_generate_p1_data(host=target_host, count=100)
