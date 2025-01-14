import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import hashlib

# MySQL Configuration
db_config = {
    "host": os.getenv("MYSQLHOST", "mysql.railway.internal"),
    "port": int(os.getenv("MYSQLPORT", 3306)),
    "user": os.getenv("MYSQLUSER", "root"),
    "password": os.getenv("MYSQLPASSWORD", "switch1998000$"),
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

app = Flask(__name__, static_folder='Markup', template_folder='Markup')
app.secret_key = '4706601636'  # Replace with a secure key

# Test the database connection on app startup
test_database_connection()

@app.route('/db-contents')
def db_contents():
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users;")  # Replace 'users' with your table name
                results = cursor.fetchall()
                
                # Create an HTML table to display the results
                html = "<h1>Database Contents</h1><table border='1'><tr><th>ID</th><th>Username</th><th>Role</th></tr>"
                for row in results:
                    html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
                html += "</table>"
                return html
        except Exception as e:
            return f"<h1>Error fetching data: {str(e)}</h1>"
        finally:
            connection.close()
    else:
        return "<h1>Failed to connect to the database.</h1>"

@app.route('/')
def login():
    return render_template('Login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()  # Hash the password

    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT role FROM users WHERE username=%s AND password_hash=%s", (username, password_hash))
                result = cursor.fetchone()
                if result:
                    session['username'] = username
                    session['role'] = result[0]
                    return redirect(url_for('dashboard'))
                else:
                    return "<h1>Login Failed: Invalid credentials</h1>"
        except Exception as e:
            return f"<h1>Error: {str(e)}</h1>"
        finally:
            connection.close()
    else:
        return "<h1>Database Connection Failed</h1>"

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"<h1>Welcome, {session['username']}! Role: {session['role']}</h1>"
    else:
        return redirect(url_for('login'))

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    import os
    port = int(os.getenv("PORT", 3306))
    app.run(host='0.0.0.0', port=port, debug=False)
