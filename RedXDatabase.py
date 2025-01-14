import os
import pymysql

# MySQL Configuration
db_config = {
    "host": os.getenv("MYSQLHOST", "mysql.railway.internal"),  # The default host for Railway or Render
    "port": int(os.getenv("MYSQLPORT", 3306)),
    "user": os.getenv("MYSQLUSER", "root"),
    "password": os.getenv("MYSQLPASSWORD", "Switch1998000$"),
    "database": os.getenv("MYSQLDATABASE", "RedXDatabase")
}

def get_db_connection():
    """Creates and returns a MySQL database connection."""
    try:
        connection = pymysql.connect(**db_config)
        print("Database connection successful!")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None

def test_database_connection():
    """Tests the database connection and prints a sample record."""
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users LIMIT 1;")  # Adjust if your table name is different
                result = cursor.fetchone()
                if result:
                    print(f"First record in 'users' table: {result}")
                else:
                    print("No records found in the 'users' table.")
        except pymysql.MySQLError as e:
            print(f"Error testing the database: {e}")
        finally:
            connection.close()
