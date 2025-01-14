import os
import pymysql

db_config = {
    "host": os.getenv("MYSQLHOST"),        # Provided by Railway
    "port": int(os.getenv("MYSQLPORT", 5000)),  # Default is 3306
    "user": os.getenv("MYSQLUSER"),        # Provided by Railway
    "password": os.getenv("MYSQLPASSWORD"), # Provided by Railway
    "database": os.getenv("MYSQLDATABASE")  # Provided by Railway
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
