import pymysql
import os

# Database configuration using environment variables for flexibility
db_config = {
    "host": os.getenv("MYSQLHOST", "mysql.railway.internal"),
    "port": int(os.getenv("MYSQLPORT", 3306)),
    "user": os.getenv("MYSQLUSER", "root"),
    "password": os.getenv("MYSQLPASSWORD", "Switch1998000$"),
    "database": os.getenv("MYSQLDATABASE", "RedXDatabase")
}

def test_connection():
    """Test the database connection and print available tables."""
    try:
        # Connect to the database
        connection = pymysql.connect(**db_config)
        print("Database connection successful!")
        
        # Execute a query to show tables
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            if tables:
                print("Tables:", tables)
            else:
                print("No tables found in the database.")
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")
    finally:
        # Ensure the connection is closed
        if 'connection' in locals() and connection:
            connection.close()
            print("Database connection closed.")

# Run the test connection
if __name__ == "__main__":
    test_connection()
