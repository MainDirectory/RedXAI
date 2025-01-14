from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
from RedXDatabase import get_db_connection, test_database_connection

app = Flask(__name__, static_folder='Markup', template_folder='Markup')
app.secret_key = '4706601636'  # Replace with a secure key

# Test the database connection on app startup
test_database_connection()

@app.route('/')
def login():
    return render_template('Login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode()).hexdigest()

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

@app.route('/db-contents')
def db_contents():
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users;")
                results = cursor.fetchall()

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

if __name__ == '__main__':
    import os
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
