from flask import Flask, render_template, request, redirect, url_for, session,jsonify,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import google.generativeai as genai
# from google.generativeai import get_chat_response

from flask_mail import Mail, Message

from flask import current_app


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'sudheerdata@outlook.com'
app.config['MAIL_PASSWORD'] = 'Sudheer@123'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)




from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np


csv_path = 'diabetes.csv'  
data = pd.read_csv(csv_path)

X = data[['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']]
y = data['Outcome']
X = X.to_numpy()

model1 = LinearRegression()
model1.fit(X, y)




API_KEY = 'AIzaSyCnHiPnc81WluNjSklL6lLR5FO_NbHRCfM'
#'AIzaSyCCrYnLhDIgToWeG4u_nPpQcB9uNJMze0U'
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
instruction = "In this chat, respond to medical-related queries only. If the query is not medical-related, please respond with a polite message stating that I can only answer medical questions."

medical_keywords = [
    'doctor', 'medicine', 'health', 'symptom', 'treatment', 'diagnosis', 
    'therapy', 'medical', 'hospital', 'clinic', 'pharmacy', 'nurse', 
    'emergency', 'surgery', 'physician', 'prescription', 'patient', 
    'healthcare', 'pediatrician', 'dermatologist', 'gynecologist', 
    'cardiologist', 'neurologist', 'oncologist', 'radiologist', 
    'psychiatrist', 'ophthalmologist', 'orthopedic', 'dietitian', 
    'allergist', 'chiropractor', 'podiatrist', 'medication', 'delivery', 
    'order', 'track', 'shipment', 'customer service', 'pharmacy network', 
    'health advice', 'emergency assistance', 'drug recall', 'side effects', 
    'health tips', 'medication reminder', 'privacy', 'compliance', 'regulation', 
    'data privacy', 'healthcare provider', 'first aid', 'health guide', 
    'medicine availability', 'online pharmacy', 'prescription refill', 
    'pharmacy support', 'medication information', 'drug interaction', 
    'drug safety', 'medical emergency', 'pharmacy services', 'drug delivery', 
    'medical delivery', 'patient support', 'order status', 'payment options', 
    'drug compatibility', 'pharmaceutical care', 'patient care', 'medicine use', 
    'healthcare advice', 'prescription advice', 'medication order', 'prescription order', 
    'medication guidance', 'pharmacy assistance', 'healthcare support',
    'consultation', 'doctor consultation', 'medical advice', 'health consultation', 
    'telemedicine', 'virtual consultation', 'medical specialist', 'doctor appointment', 
    'online doctor', 'specialist consultation', 'second opinion', 'health specialist', 
    'medical consultation', 'physician consultation', 'GP consultation', 'doctor visit', 
    'health check', 'medical opinion', 'medical referral', 'remote consultation',
    'lab test', 'blood test', 'urine test', 'diagnostic test', 'pathology', 
    'laboratory', 'lab technician', 'test result', 'lab procedure', 
    'medical test', 'clinical test', 'biopsy', 'culture test', 'genetic test', 
    'microbiology test', 'serology test', 'immunology test', 'radiology test', 
    'PCR test', 'MRI scan', 'CT scan', 'X-ray', 'ultrasound'
]







app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sudheer@123'
app.config['MYSQL_DB'] = 'medicaldelivery103'

mysql = MySQL(app)

# @app.route('/')
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         username = request.form['username']
#         password = request.form['password']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
#         account = cursor.fetchone()
#         if account:
#             session['loggedin'] = True
#             session['id'] = account['id']
#             session['username'] = account['username']
#             session['mail']=account['email']
#             if username == 'admin':
#                 return redirect(url_for('admin_home'))
#             else:
#                 return redirect(url_for('index'))
#         else:
#             msg = 'Incorrect username/password!'
#     return render_template('login.html', msg=msg)


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
            session['mail'] = account['email']
            if username == 'admin':
                return render_template('admin1.html')
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





@app.route('/ml', methods=['GET', 'POST'])
def homee():
    if request.method == 'POST':
        inputs = [float(request.form[field]) for field in ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']]
        prediction = model1.predict([inputs])
        output = "Diabetic" if prediction[0] >= 0.5 else "Not Diabetic"
        return render_template('index1.html', prediction_text=f'The person is {output}')
    return render_template('index1.html')


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
        cursor.execute("""
            SELECT cart.id AS cart_id, medicines.id AS id, medicines.name, medicines.price, cart.quantity 
            FROM cart 
            JOIN medicines ON cart.medicine_id = medicines.id 
            WHERE cart.user_id = %s
        """, (session['id'],))
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



@app.route('/sendemail', methods=['GET', 'POST'])
def sendemail():
    if request.method == 'POST':
        email = request.form['email']
        message_body = request.form['message']
        message = Message('Mail from Medical Delivery System', sender='MED24', recipients=[email])
        message.body = message_body
        mail.send(message)
        return 'Mail sent successfully!'
    return render_template('sendemail.html')





@app.route('/checkout', methods=['POST'])
def checkout():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT medicines.name, cart.quantity, medicines.price,medicines.id 
            FROM cart 
            JOIN medicines ON cart.medicine_id = medicines.id 
            WHERE cart.user_id = %s
        """, (session['id'],))
        cart_items = cursor.fetchall()
        
        email = session.get('email')
        if not email:
            cursor.execute('SELECT email FROM users WHERE id = %s', (session['id'],))
            user = cursor.fetchone()
            email = user['email']

        message_body = 'Thank you for your order. Here are the details:\n\n'
        for item in cart_items:
            message_body += f"{item['name']} - Quantity: {item['quantity']} - Price: ₹{item['price'] * item['quantity']}\n"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''
            INSERT INTO orders (user_id, medicine_id,quantity) 
            values (%s,%s,%s)''',(session['id'],item['id'],item['quantity'],))

        
        message = Message('Order Confirmation', sender='sudheerdata@outlook.com', recipients=[email])
        message.body = message_body
        mail.send(message)

        
        
        cursor.execute('DELETE FROM cart WHERE user_id = %s', (session['id'],))
        mysql.connection.commit()
        
        return redirect(url_for('index'))
    return redirect(url_for('login'))




@app.route('/admin_home')
def admin_home():
    if 'loggedin' in session and session['username'] == 'admin':
        return render_template('admin1.html')
    return redirect(url_for('login'))





@app.route('/adminmed')
def admin_medicines():
    if 'loggedin' in session and session['username'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM medicines')
        medicines = cursor.fetchall()
        return render_template('adminmed.html', medicines=medicines)
    return redirect(url_for('login'))

@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    if 'loggedin' in session and session['username'] == 'admin':
        name = request.form['name']
        price = request.form['price']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO medicines (name, price) VALUES (%s, %s)', (name, price))
        mysql.connection.commit()
        return redirect(url_for('admin_medicines'))
    return redirect(url_for('login'))

@app.route('/delete_medicine/<int:medicine_id>', methods=['POST'])
def delete_medicine(medicine_id):
    if 'loggedin' in session and session['username'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM medicines WHERE id = %s', (medicine_id,))
        mysql.connection.commit()
        return redirect(url_for('admin_medicines'))
    return redirect(url_for('login'))

@app.route('/admindoct')
def admin_doctors():
    if 'loggedin' in session and session['username'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctors')
        doctors = cursor.fetchall()
        return render_template('admindoct.html', doctors=doctors)
    return redirect(url_for('login'))

@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    if 'loggedin' in session and session['username'] == 'admin':
        name = request.form['name']
        specialty = request.form['specialty']
        consultation_fee = request.form['consultation_fee']
        doctor_status = request.form['doctors_status']
        
        if not (name and specialty and consultation_fee):
            flash('Please fill out all required fields.', 'error')
            return redirect(url_for('admin_doctors'))
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO doctors (name, specialty, consultation_fee, doctors_status) VALUES (%s, %s, %s, %s)',
                       (name, specialty, consultation_fee, doctor_status))
        mysql.connection.commit()
        cursor.close()
        
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('admin_doctors'))
    
    return redirect(url_for('login'))


@app.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    if 'loggedin' in session and session['username'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM doctors WHERE id = %s', (doctor_id,))
        mysql.connection.commit()
        return redirect(url_for('admin_doctors'))
    return redirect(url_for('login'))

@app.route('/adminlab')
def admin_lab_tests():
    if 'loggedin' in session and session['username'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM lab_tests')
        lab_tests = cursor.fetchall()
        return render_template('adminlab.html', lab_tests=lab_tests)
    return redirect(url_for('login'))

@app.route('/add_lab_test', methods=['POST'])
def add_lab_test():
    if 'loggedin' in session and session['username'] == 'admin':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        
        if not (name and description and price):
            flash('Please fill out all required fields.', 'error')
            return redirect(url_for('admin_lab_tests'))
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO lab_tests (name, description, price) VALUES (%s, %s, %s)', (name, description, price))
        mysql.connection.commit()
        cursor.close()
        
        flash('Lab Test added successfully!', 'success')
        return redirect(url_for('admin_lab_tests'))
    
    return redirect(url_for('login'))

@app.route('/delete_lab_test/<int:lab_test_id>', methods=['POST'])
def delete_lab_test(lab_test_id):
    if 'loggedin' in session and session['username'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM lab_tests WHERE id = %s', (lab_test_id,))
        mysql.connection.commit()
        return redirect(url_for('admin_lab_tests'))
    return redirect(url_for('login'))

@app.route('/adminord')
def admin_orders():
    if 'loggedin' in session and session['username'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT orders.id, medicines.name AS medicine_name, users.username, medicines.price, orders.status 
            FROM orders 
            JOIN medicines ON orders.medicine_id = medicines.id 
            JOIN users ON orders.user_id = users.id
        ''')
        orders = cursor.fetchall()
        return render_template('adminord.html', orders=orders)
    return redirect(url_for('login'))

@app.route('/update_order/<int:order_id>', methods=['POST'])
def update_order(order_id):
    if 'loggedin' in session and session['username'] == 'admin':
        status = request.form['status']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE orders SET status = %s WHERE id = %s', (status, order_id))
        mysql.connection.commit()
        return redirect(url_for('admin_orders'))
    return redirect(url_for('login'))

 


@app.route('/consultation1')
def consultation1():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Fetch doctors
        cursor.execute('SELECT * FROM doctors')
        doctors = cursor.fetchall()
        
        return render_template('consultation.html', doctors=doctors)
    
    return redirect(url_for('login'))




@app.route('/lab_tests1')
def lab_tests1():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM lab_tests1')
        lab_tests = cursor.fetchall()
        return render_template('lab_tests.html', lab_tests1=lab_tests1)
    return redirect(url_for('login'))


@app.route('/basic_health_screening')
def basic_health_screening():
    tests = ["Complete Blood Count (CBC)", "Basic Metabolic Panel (BMP)"]
    return  render_template("basic_health_screening.html",title="Basic Health Screening", tests=tests)

@app.route('/cardiovascular_health')
def cardiovascular_health():
    tests = ["High-Sensitivity C-Reactive Protein (hs-CRP)"]
    return render_template('cardiovascular_health.html', title="Cardiovascular Health", tests=tests)

@app.route('/diabetes_management')
def diabetes_management():
        tests = [
            "Fasting Blood Sugar (FBS)",
            "Hemoglobin A1c (HbA1c)"
        ]
        return render_template('diabetes_management.html', title="Diabetes Management", tests=tests)

@app.route('/thyroid_function')
def thyroid_function():
        tests = [
            "Thyroid Stimulating Hormone (TSH)",
            "Free T4 (Thyroxine)",
            "Free T3 (Triiodothyronine)"
        ]
        return render_template('thyroid_function.html', title="Thyroid Function", tests=tests)

@app.route('/liver_function')
def liver_function():
        tests = [
            "Liver Function Tests (LFTs)",
            "Albumin"
        ]
        return render_template('liver_function.html', title="Liver Function", tests=tests)

@app.route('/kidney_function')
def kidney_function():
        tests = [
            "Blood Urea Nitrogen (BUN)",
            "Serum Creatinine",
            "Estimated Glomerular Filtration Rate (eGFR)"
        ]
        return render_template('kidney_function.html', title="Kidney Function", tests=tests)

@app.route('/infection_and_inflammation')
def infection_and_inflammation():
        tests = [
            "C-Reactive Protein (CRP)",
            "Erythrocyte Sedimentation Rate (ESR)",
            "Blood Cultures"
        ]
        return render_template('infection_and_inflammation.html', title="Infection and Inflammation", tests=tests)

@app.route('/nutritional_and_vitamin_levels')
def nutritional_and_vitamin_levels():
        tests = [
            "Vitamin D Test",
            "Iron Studies"
        ]
        return render_template('nutritional_and_vitamin_levels.html', title="Nutritional and Vitamin Levels", tests=tests)

@app.route('/hormonal_panels')
def hormonal_panels():
        tests = [
            "Estrogen and Progesterone",
            "Testosterone",
            "Cortisol",
            "Prolactin"
        ]
        return render_template('hormonal_panels.html', title="Hormonal Panels", tests=tests)

@app.route('/reproductive_health')
def reproductive_health():
        tests = [
            "Human Chorionic Gonadotropin (hCG)",
            "Follicle-Stimulating Hormone (FSH)",
            "Luteinizing Hormone (LH)"
        ]
        return render_template('reproductive_health.html', title="Reproductive Health", tests=tests)

@app.route('/autoimmune_disorders')
def autoimmune_disorders():
        tests = [
            "Antinuclear Antibodies (ANA)",
            "Rheumatoid Factor (RF)"
        ]
        return render_template('autoimmune_disorders.html', title="Autoimmune Disorders", tests=tests)

@app.route('/allergy_testing')
def allergy_testing():
        tests = [
            "IgE Antibody Test",
            "Skin Prick Test"
        ]
        return render_template('allergy_testing.html', title="Allergy Testing", tests=tests)

@app.route('/cancer_markers')
def cancer_markers():
        tests = [
            "Prostate-Specific Antigen (PSA)",
            "CA-125",
            "Carcinoembryonic Antigen (CEA)"
        ]
        return render_template('cancer_markers.html', title="Cancer Markers", tests=tests)

@app.route('/genetic_testing')
def genetic_testing():
        tests = [
            "BRCA1 and BRCA2",
            "Carrier Screening"
        ]
        return render_template('genetic_testing.html', title="Genetic Testing", tests=tests)

@app.route('/infectious_diseases')
def infectious_diseases():
        tests = [
            "HIV Test",
            "Hepatitis Panel",
            "Tuberculosis (TB) Test"
        ]
        return render_template('infectious_diseases.html', title="Infectious Diseases", tests=tests)

@app.route('/urine_tests')
def urine_tests():
        tests = [
            "Urinalysis",
            "Urine Culture"
        ]
        return render_template('urine_tests.html', title="Urine Tests", tests=tests)

@app.route('/bone_health')
def bone_health():
        tests = [
            "Bone Mineral Density (BMD) Test",
            "Calcium Test"
        ]
        return render_template('bone_health.html', title="Bone Health", tests=tests)

@app.route('/electrolyte_and_fluid_balance')
def electrolyte_and_fluid_balance():
        tests = [
            "Sodium Test",
            "Potassium Test",
            "Chloride Test",
            "Bicarbonate Test"
        ]
        return render_template('electrolyte_and_fluid_balance.html', title="Electrolyte and Fluid Balance", tests=tests)

@app.route('/gastrointestinal_health')
def gastrointestinal_health():
        tests = [
            "Helicobacter pylori (H. pylori) Test",
            "Celiac Disease Panel",
            "Lactose Intolerance Test"
        ]
        return render_template('gastrointestinal_health.html', title="Gastrointestinal Health", tests=tests)

@app.route('/toxicology_and_drug_testing')
def toxicology_and_drug_testing():
        tests = [
            "Drug Abuse Panel",
            "Heavy Metals Panel",
            "Alcohol Testing"
        ]
        return render_template('toxicology_and_drug_testing.html', title="Toxicology and Drug Testing", tests=tests)

@app.route('/immunology_and_serology')
def immunology_and_serology():
        tests = [
            "Immunoglobulin Levels (IgA, IgG, IgM)",
            "Rubella Antibody Test",
            "Hepatitis Serology"
        ]
        return render_template('immunology_and_serology.html', title="Immunology and Serology", tests=tests)

@app.route('/endocrine_system')
def endocrine_system():
    tests = [
"Adrenocorticotropic Hormone (ACTH)",
"Parathyroid Hormone (PTH)",
"Insulin Test"
]
    return render_template('endocrine_system.html', title="Endocrine System", tests=tests)

@app.route('/rheumatology')
def rheumatology():
    tests = [
"Anticitrullinated Protein Antibody (ACPA)",
"Anti-Smith (Anti-Sm) Antibodies"
]
    return render_template('rheumatology.html', title="Rheumatology", tests=tests)

@app.route('/neurology')
def neurology():
    tests = [
"Electroencephalogram (EEG)",
"Nerve Conduction Studies"
]
    return render_template('neurology.html', title="Neurology", tests=tests)

@app.route('/ophthalmology')
def ophthalmology():
    tests = [
"Ocular Pressure Test (Tonometry)",
"Retinal Exam"
]
    return render_template('ophthalmology.html', title="Ophthalmology", tests=tests)

@app.route('/dermatology')
def dermatology():
    tests = [
"Skin Biopsy",
"Patch Testing"
]
    return render_template('dermatology.html', title="Dermatology", tests=tests)


@app.route('/tests_by_pincode', methods=['POST'])
def tests_by_pincode():
        pincode = request.form.get('pincode')
        tests_by_pincode_data = {
            '123456': ['Basic Health Screening', 'Cardiovascular Health'],
            '789012': ['Diabetes Management', 'Liver Function'],
            '345678': ['Thyroid Function', 'Kidney Function'],
            '111222': ['Infection and Inflammation'],
            '333444': ['Nutritional and Vitamin Levels'],
            '555666': ['Hormonal Panels'],
            '777888': ['Reproductive Health'],
            '999000': ['Autoimmune Disorders'],
            '121212': ['Allergy Testing'],
            '232323': ['Cancer Markers'],
            '343434': ['Genetic Testing'],
            '454545': ['Infectious Diseases'],
            '565656': ['Urine Tests'],
            '676767': ['Bone Health'],
            '787878': ['Electrolyte and Fluid Balance'],
            '898989': ['Gastrointestinal Health'],
            '909090': ['Toxicology and Drug Testing'],
            '101010': ['Immunology and Serology'],
            '111111': ['Endocrine System'],
            '121212': ['Rheumatology'],
            '131313': ['Dermatology'],
            '141414': ['Ophthalmology'],
            '151515': ['Neurology']
        }

        tests = tests_by_pincode_data.get(pincode, [])

        if not tests:
            flash('No tests available for this pincode', 'danger')
            return redirect(url_for('lab_tests1'))

        return render_template('tests_by_pincode.html', pincode=pincode, tests=tests)






@app.route('/lab_tests')
def lab_tests():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Fetch lab tests
        cursor.execute('SELECT * FROM lab_tests')
        lab_tests = cursor.fetchall()
        
        return render_template('lab_test.html', lab_tests=lab_tests)
    
    return redirect(url_for('login'))


from flask import flash

@app.route('/book_consultation', methods=['POST'])
def book_consultation():
    if 'loggedin' in session:
        doctor_id = request.form['consultation_id']
        consultation_date = request.form['date']
        consultation_time = request.form['time']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Corrected SQL query to fetch consultation_fee and name
        cursor.execute('SELECT consultation_fee, name FROM doctors WHERE id = %s', (doctor_id,))
        doctor = cursor.fetchone()
        
        if doctor:
            consultation_fee = doctor['consultation_fee']
            doctor_name = doctor['name']
            
            cursor.execute('INSERT INTO consultations (user_id, doctor_id, doctor_name, consultation_date, consultation_time, consultation_fee) VALUES (%s, %s, %s, %s, %s, %s)', 
                           (session['id'], doctor_id, doctor_name, consultation_date, consultation_time, consultation_fee))
            mysql.connection.commit()
            
            flash('Consultation booked successfully', 'success')
        else:
            flash('Doctor not found', 'error')
        
        cursor.close()
        return redirect(url_for('index')) 
        
    return redirect(url_for('login'))  




@app.route('/schedule_lab_test', methods=['POST'])
def schedule_lab_test():
    if 'loggedin' in session:
        lab_test_id = request.form['lab_test_id']
        date = request.form['date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO user_lab_tests (user_id, lab_test_id, date) VALUES (%s, %s, %s)', (session['id'], lab_test_id, date))
        mysql.connection.commit()
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/past_consultations')
def past_consultations():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT c.id, c.doctor_id, d.name AS doctor_name, c.consultation_date, c.consultation_time, c.consultation_fee
            FROM consultations c
            JOIN doctors d ON c.doctor_id = d.id
            WHERE c.user_id = %s
        ''', (session['id'],))
        consultations = cursor.fetchall()
        return render_template('past_consultations.html', consultations=consultations)
    return redirect(url_for('login'))


@app.route('/past_lab_bookings')
def past_lab_bookings():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT ult.*, lt.name as lab_test_name 
            FROM user_lab_tests ult 
            JOIN lab_tests lt ON ult.lab_test_id = lt.id 
            WHERE ult.user_id = %s
        ''', (session['id'],))
        lab_bookings = cursor.fetchall()
        return render_template('past_lab_bookings.html', lab_bookings=lab_bookings)
    return redirect(url_for('login'))



@app.route('/chat')
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = str(request.form['messageText'])
    
    if not is_medical_query(user_message):
        bot_response_text = "I'm sorry, I can only answer medical-related questions. Please ask a question related to medical topics."
    else:
        bot_response = chat.send_message(user_message)
        bot_response_text = bot_response.text
    
    return jsonify({'status': 'OK', 'answer': bot_response_text})

def is_medical_query(query):
    return any(keyword in query.lower() for keyword in medical_keywords)







if __name__ == '__main__':
    app.run(debug=True,port=7003)