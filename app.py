from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sudheer@123'
app.config['MYSQL_DB'] = 'medicaldelivery'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            if username == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            msg = 'Incorrect username/password!'
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
    if request.method == 'POST' and all(field in request.form for field in ['username', 'password', 'email', 'address', 'city', 'state', 'country', 'postalcode', 'medical_condition']):
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        medical_condition = request.form['medical_condition']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            cursor.execute('INSERT INTO users (username, password, email, medical_condition, address, city, state, country, postalcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (username, password, email, medical_condition, address, city, state, country, postalcode,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/index')
def index():
    if 'loggedin' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/display')
def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('display.html', account=account)
    return redirect(url_for('login'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        if request.method == 'POST' and account and all(key in request.form for key in ['username', 'password', 'email', 'address', 'city', 'state', 'country', 'postalcode', 'medical_condition']):
            try:
                username = request.form['username']
                password = request.form['password']
                email = request.form['email']
                medical_condition = request.form['medical_condition']
                address = request.form['address']
                city = request.form['city']
                state = request.form['state']
                country = request.form['country']
                postalcode = request.form['postalcode']
                cursor.execute('SELECT * FROM users WHERE username = %s AND id != %s', (username, session['id'],))
                existing_account = cursor.fetchone()
                if existing_account:
                    msg = 'Username already taken by another account!'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address!'
                elif not re.match(r'[A-Za-z0-9]+', username):
                    msg = 'Username must contain only characters and numbers!'
                else:
                    cursor.execute('UPDATE users SET username = %s, password = %s, email = %s, medical_condition = %s, address = %s, city = %s, state = %s, country = %s, postalcode = %s WHERE id = %s', 
                                   (username, password, email, medical_condition, address, city, state, country, postalcode, session['id'],))
                    mysql.connection.commit()
                    msg = 'You have successfully updated!'
            except Exception as e:
                msg = f'An error occurred: {str(e)}'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('update.html', msg=msg, account=account)
    return redirect(url_for('login'))

@app.route('/medicines')
def medicines():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM medicines')
        medicines = cursor.fetchall()
        return render_template('medicines.html', medicines=medicines)
    return redirect(url_for('login'))

@app.route('/add_to_cart/<int:medicine_id>')
def add_to_cart(medicine_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO cart (user_id, medicine_id) VALUES (%s, %s)', (session['id'], medicine_id))
        mysql.connection.commit()
        return redirect(url_for('cart'))
    return redirect(url_for('login'))

@app.route('/cart')
def cart():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT cart.id AS cart_id, medicines.id AS id, medicines.name, medicines.price, cart.quantity 
            FROM cart 
            JOIN medicines ON cart.medicine_id = medicines.id 
            WHERE cart.user_id = %s
        ''', (session['id'],))
        cart_items = cursor.fetchall()
        return render_template('cart.html', cart_items=cart_items)
    return redirect(url_for('login'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    if 'loggedin' in session:
        medicine_id = request.form['medicine_id']
        quantity = request.form['quantity']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE cart SET quantity = %s WHERE user_id = %s AND medicine_id = %s', (quantity, session['id'], medicine_id))
        mysql.connection.commit()
        return redirect(url_for('cart'))
    return redirect(url_for('login'))

@app.route('/delete_from_cart', methods=['POST'])
def delete_from_cart():
    if 'loggedin' in session:
        medicine_id = request.form['medicine_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM cart WHERE user_id = %s AND medicine_id = %s', (session['id'], medicine_id))
        mysql.connection.commit()
        return redirect(url_for('cart'))
    return redirect(url_for('login'))

@app.route('/checkout')
def checkout():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            INSERT INTO orders (user_id, medicine_id) 
            SELECT user_id, medicine_id FROM cart WHERE user_id = %s
        ''', (session['id'],))
        cursor.execute('DELETE FROM cart WHERE user_id = %s', (session['id'],))
        mysql.connection.commit()
        return redirect(url_for('orders'))
    return redirect(url_for('login'))

@app.route('/orders')
def orders():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT medicines.name, medicines.price 
            FROM orders 
            JOIN medicines ON orders.medicine_id = medicines.id 
            WHERE orders.user_id = %s
        ''', (session['id'],))
        orders = cursor.fetchall()
        return render_template('orders.html', orders=orders)
    return redirect(url_for('login'))


@app.route('/admin')
def admin_dashboard():
    if 'loggedin' in session and session['username'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM medicines')
        medicines = cursor.fetchall()
        cursor.execute('''
            SELECT orders.id, medicines.name AS medicine_name, users.username, medicines.price, orders.status 
            FROM orders 
            JOIN medicines ON orders.medicine_id = medicines.id 
            JOIN users ON orders.user_id = users.id
        ''')
        orders = cursor.fetchall()
        return render_template('admin.html', medicines=medicines, orders=orders)
    return redirect(url_for('login'))

@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    if 'loggedin' in session and session['username'] == 'admin':
        name = request.form['name']
        price = request.form['price']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO medicines (name, price) VALUES (%s, %s)', (name, price))
        mysql.connection.commit()
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))



@app.route('/delete_medicine/<int:medicine_id>', methods=['POST'])
def delete_medicine(medicine_id):
    if 'loggedin' in session and session['username'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM medicines WHERE id = %s', (medicine_id,))
        mysql.connection.commit()
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))


@app.route('/update_order/<int:order_id>', methods=['POST'])
def update_order(order_id):
    if 'loggedin' in session and session['username'] == 'admin':
        status = request.form['status']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE orders SET status = %s WHERE id = %s', (status, order_id))
        mysql.connection.commit()
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))



@app.route('/order_tracking')
def order_tracking():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT orders.id AS order_id, medicines.name AS medicine_name, orders.quantity, orders.order_date, orders.status
            FROM orders
            JOIN medicines ON orders.medicine_id = medicines.id
            WHERE orders.user_id = %s
        ''', (session['id'],))
        orders = cursor.fetchall()
        return render_template('order_tracking.html', orders=orders)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = 5000  
    print(f"Starting Flask app on port {port}")
    app.run(debug=True, port=port)
