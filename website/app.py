from flask import Flask, render_template, request, redirect, session, url_for
import json
import os
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# Load accounts from the signIn directory
accounts_file = os.path.join(os.path.dirname(__file__), '..', 'signIn', 'accounts.json')

def load_accounts():
    if os.path.exists(accounts_file):
        with open(accounts_file, 'r') as f:
            return json.load(f)
    return {}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            error = 'Please fill in all fields'
        else:
            accounts = load_accounts()
            if username in accounts:
                stored_hash = accounts[username]['password_hash'].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    session['username'] = username
                    return redirect(url_for('dashboard'))
                else:
                    error = 'Invalid username or password'
            else:
                error = 'Invalid username or password'
    
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=50000)
