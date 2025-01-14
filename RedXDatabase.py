import pymysql

# MySQL Configuration
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Switch1998000$",
    "database": "redxdatabase"
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

def create_users_table():
    """Creates the 'users' table if it doesn't exist."""
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) NOT NULL UNIQUE,
                        password_hash VARCHAR(255) NOT NULL,
                        role VARCHAR(50) DEFAULT 'user',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                print("Table 'users' created or already exists.")
        except pymysql.MySQLError as e:
            print(f"Error creating 'users' table: {e}")
        finally:
            connection.close()

def test_database_connection():
    """Tests the database connection and prints a sample record."""
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users LIMIT 1;")
                result = cursor.fetchone()
                if result:
                    print(f"First record in 'users' table: {result}")
                else:
                    print("No records found in the 'users' table.")
        except pymysql.MySQLError as e:
            print(f"Error testing the database: {e}")
        finally:
            connection.close()

# Run table creation and test the database connection if the script is executed directly
if __name__ == "__main__":
    create_users_table()
    test_database_connection()
