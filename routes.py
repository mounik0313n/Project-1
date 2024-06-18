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
    return render_template('tests.html')

@main_blueprint.route('/basic_health_screening')
def basic_health_screening():
    tests = [
        "Complete Blood Count (CBC)",
        "Basic Metabolic Panel (BMP)"
    ]
    return render_template('subcategory.html', title="Basic Health Screening", tests=tests)

@main_blueprint.route('/cardiovascular_health')
def cardiovascular_health():
    tests = [
        "High-Sensitivity",
        "C-Reactive Protein (hs-CRP)"
    ]
    return render_template('subcategory.html', title="Cardiovascular Health", tests=tests)

@main_blueprint.route('/diabetes_management')
def diabetes_management():
    tests = [
        "Fasting Blood Sugar (FBS)",
        "Hemoglobin A1c (HbA1c)"
    ]
    return render_template('subcategory.html', title="Diabetes Management", tests=tests)

@main_blueprint.route('/thyroid_function')
def thyroid_function():
    tests = [
        "Thyroid Stimulating Hormone (TSH)",
        "Free T4 (Thyroxine)",
        "Free T3 (Triiodothyronine)"
    ]
    return render_template('subcategory.html', title="Thyroid Function", tests=tests)

@main_blueprint.route('/liver_function')
def liver_function():
    tests = [
        "Liver Function Tests (LFTs)",
        "Albumin"
    ]
    return render_template('subcategory.html', title="Liver Function", tests=tests)

@main_blueprint.route('/kidney_function')
def kidney_function():
    tests = [
        "Blood Urea Nitrogen (BUN)",
        "Serum Creatinine",
        "Estimated Glomerular Filtration Rate (eGFR)"
    ]
    return render_template('subcategory.html', title="Kidney Function", tests=tests)
@main_blueprint.route('/infection_and_inflammation')
def infection_and_inflammation():
    tests = [
        "C-Reactive Protein (CRP)",
        "Erythrocyte Sedimentation Rate (ESR)",
        "Blood Cultures"
    ]
    return render_template('subcategory.html', title="Infection and Inflammation", tests=tests)

@main_blueprint.route('/nutritional_and_vitamin_levels')
def nutritional_and_vitamin_levels():
    tests = [
        "Vitamin D Test",
        "Iron Studies"
    ]
    return render_template('subcategory.html', title="Nutritional and Vitamin Levels", tests=tests)

@main_blueprint.route('/hormonal_panels')
def hormonal_panels():
    tests = [
        "Estrogen and Progesterone",
        "Testosterone",
        "Cortisol",
        "Prolactin"
    ]
    return render_template('subcategory.html', title="Hormonal Panels", tests=tests)

@main_blueprint.route('/reproductive_health')
def reproductive_health():
    tests = [
        "Human Chorionic Gonadotropin (hCG)",
        "Follicle-Stimulating Hormone (FSH)",
        "Luteinizing Hormone (LH)"
    ]
    return render_template('subcategory.html', title="Reproductive Health", tests=tests)

@main_blueprint.route('/autoimmune_disorders')
def autoimmune_disorders():
    tests = [
        "Antinuclear Antibodies (ANA)",
        "Rheumatoid Factor (RF)"
    ]
    return render_template('subcategory.html', title="Autoimmune Disorders", tests=tests)

@main_blueprint.route('/allergy_testing')
def allergy_testing():
    tests = [
        "IgE Antibody Test",
        "Skin Prick Test"
    ]
    return render_template('subcategory.html', title="Allergy Testing", tests=tests)

@main_blueprint.route('/cancer_markers')
def cancer_markers():
    tests = [
        "Prostate-Specific Antigen (PSA)",
        "CA-125",
        "Carcinoembryonic Antigen (CEA)"
    ]
    return render_template('subcategory.html', title="Cancer Markers", tests=tests)

@main_blueprint.route('/genetic_testing')
def genetic_testing():
    tests = [
        "BRCA1 and BRCA2",
        "Carrier Screening"
    ]
    return render_template('subcategory.html', title="Genetic Testing", tests=tests)

@main_blueprint.route('/infectious_diseases')
def infectious_diseases():
    tests = [
        "HIV Test",
        "Hepatitis Panel",
        "Tuberculosis (TB) Test"
    ]
    return render_template('subcategory.html', title="Infectious Diseases", tests=tests)

@main_blueprint.route('/urine_tests')
def urine_tests():
    tests = [
        "Urinalysis",
        "Urine Culture"
    ]
    return render_template('subcategory.html', title="Urine Tests", tests=tests)

@main_blueprint.route('/bone_health')
def bone_health():
    tests = [
        "Bone Mineral Density (BMD) Test",
        "Calcium Test"
    ]
    return render_template('subcategory.html', title="Bone Health", tests=tests)

@main_blueprint.route('/electrolyte_and_fluid_balance')
def electrolyte_and_fluid_balance():
    tests = [
        "Sodium Test",
        "Potassium Test",
        "Chloride Test",
        "Bicarbonate Test"
    ]
    return render_template('subcategory.html', title="Electrolyte and Fluid Balance", tests=tests)

@main_blueprint.route('/gastrointestinal_health')
def gastrointestinal_health():
    tests = [
        "Helicobacter pylori (H. pylori) Test",
        "Celiac Disease Panel",
        "Lactose Intolerance Test"
    ]
    return render_template('subcategory.html', title="Gastrointestinal Health", tests=tests)

@main_blueprint.route('/toxicology_and_drug_testing')
def toxicology_and_drug_testing():
    tests = [
        "Drug Abuse Panel",
        "Heavy Metals Panel",
        "Alcohol Testing"
    ]
    return render_template('subcategory.html', title="Toxicology and Drug Testing", tests=tests)

@main_blueprint.route('/immunology_and_serology')
def immunology_and_serology():
    tests = [
        "Immunoglobulin Levels (IgA, IgG, IgM)",
        "Rubella Antibody Test",
        "Hepatitis Serology"
    ]
    return render_template('subcategory.html', title="Immunology and Serology", tests=tests)

@main_blueprint.route('/endocrine_system')
def endocrine_system():
    tests = [
        "Adrenocorticotropic Hormone (ACTH)",
        "Parathyroid Hormone (PTH)",
        "Insulin Test"
    ]
    return render_template('subcategory.html', title="Endocrine System", tests=tests)

@main_blueprint.route('/rheumatology')
def rheumatology():
    tests = [
        "Anticitrullinated Protein Antibody (ACPA)",
        "Anti-Smith (Anti-Sm) Antibodies"
    ]
    return render_template('subcategory.html', title="Rheumatology", tests=tests)

@main_blueprint.route('/dermatology')
def dermatology():
    tests = [
        "Skin Biopsy",
        "Patch Testing"
    ]
    return render_template('subcategory.html', title="Dermatology", tests=tests)

@main_blueprint.route('/ophthalmology')
def ophthalmology():
    tests = [
        "Ocular Pressure Test (Tonometry)",
        "Retinal Exam"
    ]
    return render_template('subcategory.html', title="Ophthalmology", tests=tests)

@main_blueprint.route('/neurology')
def neurology():
    tests = [
        "Electroencephalogram (EEG)",
        "Nerve Conduction Studies"
    ]
    return render_template('subcategory.html', title="Neurology", tests=tests)


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

@main_blueprint.route('/tests_by_pincode', methods=['POST'])
def tests_by_pincode():
    pincode = request.form.get('pincode')
    tests = tests_by_pincode_data.get(pincode, [])

    if not tests:
        flash('No tests available for this pincode', 'danger')
        return redirect(url_for('main.tests'))

    return render_template('tests_by_pincode.html', pincode=pincode, tests=tests)

@main_blueprint.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    test_name = request.form.get('test_name')
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(test_name)
    flash(f'{test_name} added to cart!', 'success')
    return redirect(url_for('main.tests'))

@main_blueprint.route('/view_cart')
def view_cart():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('main.tests'))
    return render_template('view_cart.html', cart=session['cart'])


@main_blueprint.route('/book_test', methods=['GET', 'POST'])
def book_test():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        age = request.form['age']
        gender = request.form['gender']
        test_type = request.form['test_type']
        user_id = session.get('user_id')
        if not user_id:
            flash('Please log in to book a test.', 'danger')
            return redirect(url_for('main.login'))
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO bookings (user_id, name, address, age, gender, test_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, name, address, age, gender, test_type))
        mysql.connection.commit()
        cur.close()

        flash('Test booked successfully!', 'success')
        return redirect(url_for('main.profile'))
    selected_test = request.args.get('test_type', '')
    cur = mysql.connection.cursor()
    cur.execute("SELECT test_name FROM tests")
    available_tests = [row[0] for row in cur.fetchall()]
    cur.close()
    return render_template('book_test.html', available_tests=available_tests, selected_test=selected_test)
