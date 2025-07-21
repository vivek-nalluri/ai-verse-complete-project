from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import subprocess
import sys
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MongoDB Atlas Configuration
client = MongoClient("mongodb+srv://vivek94947:Vivek9494@cluster0.p9bhhfh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['ai_verse_db']  # database name
users_collection = db['users']  # collection name

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        full_name = request.form['full_name']

        if not username or not password or not email or not full_name:
            flash('All fields except phone are required!', 'danger')
            return render_template('register.html')

        password_hash = generate_password_hash(password)

        try:
            # Check if user or email already exists
            if users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
                flash('Username or email already exists.', 'danger')
                return render_template('register.html')

            users_collection.insert_one({
                "username": username,
                "password": password_hash,
                "email": email,
                "phone": phone,
                "full_name": full_name
            })
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            print("MongoDB insert error:", e)
            flash('Database error occurred. Try again.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Both fields are required!', 'danger')
            return render_template('login.html')

        try:
            user = users_collection.find_one({"username": username})

            if user and check_password_hash(user['password'], password):
                session['username'] = user['username']
                flash('Welcome back!', 'success')

                try:
                    subprocess.Popen(
                        [sys.executable, os.path.join(os.getcwd(), "app.py")],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                except Exception as e:
                    flash(f"Error launching app.py: {str(e)}", 'danger')

                return redirect('http://localhost:7860')

            else:
                flash('Invalid credentials. Please try again.', 'danger')

        except Exception as e:
            flash('Login failed. Try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
