from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import mysql, bcrypt

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        flash('You have successfully signed up!', 'success')
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html')

@main_blueprint.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to view this page', 'danger')
        return redirect(url_for('main.login'))
    return render_template('profile.html')

@main_blueprint.route('/tests')
def tests():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tests")
    tests = cur.fetchall()
    cur.close()
    return render_template('tests.html', tests=tests)

