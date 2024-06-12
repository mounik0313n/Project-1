from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re
import random

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'geekprofile'

# Initialize MySQL
mysql = MySQL(app)

# Set secret key for session management
app.secret_key = 'your_secret_key'

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully!'
            return redirect(url_for('index'))
        else:
            msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and all(key in request.form for key in ['username', 'password', 'email', 'address', 'city', 'country', 'postalcode', 'organisation']):
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        organisation = request.form['organisation']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                           (username, password, email, organisation, address, city, state, country, postalcode))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route("/index")
def index():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM appointments WHERE user_id = %s', (session['id'],))
        bookings = cursor.fetchall()
        return render_template("index.html", bookings=bookings)
    return redirect(url_for('login'))

@app.route("/display")
def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template("display.html", account=account)
    return redirect(url_for('login'))

@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and all(key in request.form for key in ['username', 'password', 'email', 'address', 'city', 'country', 'postalcode', 'organisation']):
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            organisation = request.form['organisation']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account and account[0] != session['id']:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            else:
                cursor.execute('UPDATE accounts SET username = %s, password = %s, email = %s, organisation = %s, address = %s, city = %s, state = %s, country = %s, postalcode = %s WHERE id = %s', 
                               (username, password, email, organisation, address, city, state, country, postalcode, session['id']))
                mysql.connection.commit()
                msg = 'You have successfully updated!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))

@app.route("/book", methods=['POST'])
def book():
    if 'loggedin' in session:
        user_id = session['id']
        name = request.form['name']
        appointment_date = request.form['date']
        doctor = request.form['doctor']
        
        # Generate a random appointment ID
        appointment_id = random.randint(100000, 999999)
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO appointments (id, user_id, appointment_date, doctor) VALUES (%s, %s, %s, %s)', 
                       (appointment_id, user_id, appointment_date, doctor))
        mysql.connection.commit()
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route("/bookings")
def bookings():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM appointments WHERE user_id = %s', (session['id'],))
        bookings = cursor.fetchall()
        return render_template("bookings.html", bookings=bookings)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="localhost", port=8500, debug=True)
