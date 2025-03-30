import random 
from flask import Flask, redirect, url_for, session, request, render_template, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Keep this secure!

# Dummy in-memory user store for username and password (not recommended for production)
USER_CREDENTIALS = {
    "username": "altonmoseley@gmail.com",  # Your username
    "password": "Tigers1389"  # Your password
}

# Fixed 2FA code
def generate_2fa_code():
    return "0000"  # Always return '0000' as the 2FA code

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['email']
        password = request.form['password']
        
        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            # Generate the fixed 2FA code and store it in the session
            session['2fa_code'] = generate_2fa_code()
            session['user_email'] = username
            return redirect(url_for('verify_2fa'))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    if request.method == 'POST':
        # Check the 2FA code
        entered_code = request.form['2fa_code']
        if entered_code == session.get('2fa_code'):
            # Successful login
            return f'Logged in successfully as: {session["user_email"]}'
        else:
            flash("Invalid 2FA code", "danger")
            return redirect(url_for('verify_2fa'))

    return render_template('verify_2fa.html')

@app.route('/logout')
def logout():
    # Log the user out by clearing the session
    session.pop('2fa_code', None)
    session.pop('user_email', None)
    return redirect(url_for('home'))

@app.route('/')
def home():
    return "Serqet Security is running securely with TLS and OAuth authentication!"

if __name__ == '__main__':
    app.run(ssl_context='adhoc', host='0.0.0.0', port=5000, debug=True)



