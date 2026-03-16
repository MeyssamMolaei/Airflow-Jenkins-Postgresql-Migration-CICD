import random
import string
import psycopg2 # Installation: pip install psycopg2-binary
import sys

def generate_random_name():
    first_names = [
        "John", "Jane", "Alex", "Emily", "Michael", "Sarah", "Chris", "Jessica", "David", "Laura",
        "Daniel", "Olivia", "Matthew", "Sophia", "Andrew", "Emma", "James", "Ava", "Joseph", "Isabella",
        "Ryan", "Mia", "Benjamin", "Charlotte", "William", "Amelia", "Ethan", "Harper", "Noah", "Evelyn",
        "Lucas", "Abigail", "Henry", "Ella", "Alexander", "Scarlett", "Sebastian", "Grace", "Jack", "Chloe",
        "Samuel", "Victoria", "Owen", "Riley", "Nathan", "Aria", "Gabriel", "Lily", "Caleb", "Hannah",
        "Isaac", "Zoe", "Julian", "Nora", "Levi", "Layla", "Anthony", "Ellie", "Dylan", "Aubrey",
        "Leo", "Sofia", "Thomas", "Penelope", "Charles", "Luna", "Christopher", "Madison", "Joshua", "Camila",
        "Isaiah", "Elizabeth", "Hudson", "Eleanor", "Christian", "Natalie", "Hunter", "Ruby", "Connor", "Stella",
        "Aaron", "Aurora", "Adrian", "Violet", "Jonathan", "Savannah", "Jeremiah", "Bella", "Eli", "Claire",
        "Landon", "Skylar", "Robert", "Lucy", "Nicholas", "Paisley", "Dominic", "Meyssam", "Jaxon", "Anna"
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
        "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
        "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
        "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
        "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Molaei", "Morgan", "Cooper",
        "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
        "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
        "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez"
    ]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def bulk_generate_p1_data(host="home.meyssam.ir", count=100, port=5432):
    """
    Connects to Postgres P1 and inserts random employee data.
    """
    try:
        print(f"📡 Attempting connection to {host}:{port}...")
        connection = psycopg2.connect(
            user="postgres",
            password="p1password",  
            host=host,
            port=port,
            database="source_db",
            connect_timeout=10
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
    # Usage: python3 generate_data.py [host] [port] [count]
    # Example 1 (Internal): python3 generate_data.py 10.43.166.83 5432
    # Example 2 (External): python3 generate_data.py home.meyssam.ir 30433
    
    target_host = sys.argv[1] if len(sys.argv) > 1 else "postgres-p1"
    target_port = int(sys.argv[2]) if len(sys.argv) > 2 else (5432 if ".83" in target_host or "postgres" in target_host else 30433)
    record_count = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    
    bulk_generate_p1_data(host=target_host, count=record_count, port=target_port)
