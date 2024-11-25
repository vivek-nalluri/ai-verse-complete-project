from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess
import sys
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'Vivek94947@'  # Change to your MySQL password
app.config['MYSQL_DB'] = 'user_database'

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Ensure the username and password are valid
        if not username or not password:
            flash('Both fields are required!', 'danger')
            return render_template('register.html')

        password_hash = generate_password_hash(password)

        try:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password_hash))
            mysql.connection.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            flash('Username already exists or database error. Try another username.', 'danger')
        finally:
            cursor.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Ensure the username and password are valid
        if not username or not password:
            flash('Both fields are required!', 'danger')
            return render_template('login.html')

        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):  # user[2] is the password hash
                session['username'] = user[1]
                flash('Welcome back!', 'success')

                # Launch app.py if not already running
                try:
                    subprocess.Popen(
                        [sys.executable, os.path.join(os.getcwd(), "app.py")],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                except Exception as e:
                    flash(f"Error launching app.py: {str(e)}", 'danger')

                # Redirect to app.py (Gradio app)
                return redirect('http://localhost:7860')

            else:
                flash('Invalid credentials. Please try again.', 'danger')

        except Exception as e:
            flash('An error occurred during login. Please try again later.', 'danger')
        finally:
            cursor.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
