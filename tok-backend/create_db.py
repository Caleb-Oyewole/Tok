import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database connection parameters
DB_USER = "postgres"
DB_PASSWORD = "postgres"  # Change this if your local PostgreSQL password is different
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "tok_db"

def create_database():
    try:
        # Connect to the default 'postgres' system database
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            dbname="postgres"
        )
        # Set autocommit mode so database creation SQL executes outside transaction blocks
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        # Check if database already exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}';")
        exists = cursor.fetchone()

        if not exists:
            # Create the database
            cursor.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"Success: Database '{DB_NAME}' created successfully!")
        else:
            print(f"Info: Database '{DB_NAME}' already exists.")

        cursor.close()
        connection.close()

    except Exception as error:
        print(f"Error connecting to PostgreSQL or creating database: {error}")

if __name__ == "__main__":
    create_database()