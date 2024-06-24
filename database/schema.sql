CREATE DATABASE medicaldelivery;
USE medicaldelivery;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    medical_condition VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50),
    country VARCHAR(50) NOT NULL,
    postalcode VARCHAR(20) NOT NULL
);

CREATE TABLE medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    medicine_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE CASCADE
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    medicine_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE CASCADE
);

CREATE TABLE lab_tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE user_lab_tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    lab_test_id INT NOT NULL,
    date DATE NOT NULL,
    results TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lab_test_id) REFERENCES lab_tests(id) ON DELETE CASCADE
);

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    consultation_fee INT NOT NULL
);

CREATE TABLE consultations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    doctor_id INT NOT NULL,
    consultation_date DATE NOT NULL,
    notes TEXT,
    consultation_fee INT NOT NULL,
    consultation_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);


INSERT INTO medicines (name, price) VALUES 
('Paracetamol', 1.00),
('Ibuprofen', 1.50),
('Amoxicillin', 3.00),
('Aspirin', 2.00),
('Cough Syrup', 4.50),
('Antacid', 2.50),
('Vitamin C', 3.00),
('Insulin', 5.00),
('Hydrochlorothiazide', 50.00),
('Prednisone', 70.00),
('Losartan', 55.00),
('Levothyroxine', 65.00),
('Atorvastatin', 80.00),
('Clopidogrel', 45.00),
('Fluoxetine', 90.00),
('Warfarin', 85.00),
('Simvastatin', 75.00),
('Montelukast', 60.00),
('Loratadine', 25.00),
('Metoprolol', 40.00),
('Furosemide', 50.00),
('Gabapentin', 85.00),
('Tramadol', 95.00),
('Citalopram', 70.00),
('Azithromycin', 120.00),
('Doxycycline', 110.00),
('Escitalopram', 105.00),
('Albuterol', 130.00);
INSERT INTO lab_tests (name, description, price) VALUES 
('Complete Blood Count (CBC)', 'A test used to evaluate your overall health and detect a variety of disorders, including anemia, infection, and leukemia.', 50.00),
('Lipid Profile', 'A panel of blood tests that serves as an initial broad medical screening tool for abnormalities in lipids, such as cholesterol and triglycerides.', 75.00),
('Liver Function Test (LFT)', 'A group of blood tests that provide information about the state of a patient\'s liver.', 60.00),
('Kidney Function Test (KFT)', 'Tests used to check how well the kidneys are working.', 65.00),
('Thyroid Function Test (TFT)', 'A collective term for blood tests used to check the function of the thyroid.', 80.00),
('Blood Glucose Test', 'A test that measures the amount of glucose (sugar) in your blood.', 40.00);

INSERT INTO doctors (name, specialty, consultation_fee)
VALUES
    ('Dr. Anil Mehta', 'Cardiology', 1500),
    ('Dr. Priya Sharma', 'Neurology', 1800),
    ('Dr. Rajesh Kapoor', 'Orthopedics', 1200),
    ('Dr. Sunita Verma', 'Dermatology', 1000),
    ('Dr. Vikram Singh', 'Pediatrics', 800),
    ('Dr. Ayesha Khan', 'Gynecology', 1300),
    ('Dr. Arjun Gupta', 'ENT', 900),
    ('Dr. Ramesh Rao', 'Ophthalmology', 1100),
    ('Dr. Neha Jain', 'Endocrinology', 1600),
    ('Dr. Mohit Chawla', 'Urology', 1400),
    ('Dr. Kavita Patel', 'Psychiatry', 1700),
    ('Dr. Rahul Sinha', 'Gastroenterology', 1500),
    ('Dr. Preeti Agarwal', 'Pulmonology', 1200),
    ('Dr. Suresh Iyer', 'Nephrology', 1600),
    ('Dr. Anjali Bhatt', 'Oncology', 2000),
    ('Dr. Sanjay Desai', 'Cardiology', 1600),
    ('Dr. Manisha Roy', 'Neurology', 1700),
    ('Dr. Abhishek Mukherjee', 'Orthopedics', 1100),
    ('Dr. Shalini Rao', 'Dermatology', 900),
    ('Dr. Vishal Tyagi', 'Pediatrics', 850),
    ('Dr. Ritu Gupta', 'Gynecology', 1250),
    ('Dr. Aniruddh Bose', 'ENT', 950),
    ('Dr. Megha Narang', 'Ophthalmology', 1150),
    ('Dr. Sneha Patel', 'Endocrinology', 1550),
    ('Dr. Kunal Thakkar', 'Urology', 1450),
    ('Dr. Parvati Rao', 'Psychiatry', 1750),
    ('Dr. Siddharth Nair', 'Gastroenterology', 1400),
    ('Dr. Arpita Singh', 'Pulmonology', 1300),
    ('Dr. Vivek Menon', 'Nephrology', 1650),
    ('Dr. Aparna Joshi', 'Oncology', 2100),
    ('Dr. Hitesh Malhotra', 'Cardiology', 1500),
    ('Dr. Nandini Das', 'Neurology', 1800),
    ('Dr. Prashant Reddy', 'Orthopedics', 1200),
    ('Dr. Anjana Ghosh', 'Dermatology', 1000),
    ('Dr. Rajiv Bansal', 'Pediatrics', 800),
    ('Dr. Savita Kapoor', 'Gynecology', 1300),
    ('Dr. Deepak Sharma', 'ENT', 900),
    ('Dr. Ritika Sen', 'Ophthalmology', 1100),
    ('Dr. Vikas Gupta', 'Endocrinology', 1600),
    ('Dr. Neeraj Agarwal', 'Urology', 1400),
    ('Dr. Pallavi Mehta', 'Psychiatry', 1700),
    ('Dr. Rohit Sinha', 'Gastroenterology', 1500),
    ('Dr. Sunil Kumar', 'Pulmonology', 1200),
    ('Dr. Aarti Patel', 'Nephrology', 1600),
    ('Dr. Rajesh Gupta', 'Oncology', 2000);


CREATE TABLE lab_tests1(
    id INT AUTO_INCREMENT PRIMARY KEY,
	category VARCHAR(255) NOT NULL,
    test_name VARCHAR(255) NOT NULL
);
INSERT INTO lab_tests1 (category, test_name) VALUES
('Basic Health Screening', 'Complete Blood Count (CBC)'),
('Basic Health Screening', 'Basic Metabolic Panel (BMP)'),
('Cardiovascular Health', 'High-Sensitivity C-Reactive Protein (hs-CRP)'),
('Diabetes Management', 'Fasting Blood Sugar (FBS)'),
('Diabetes Management', 'Hemoglobin A1c (HbA1c)'),
('Thyroid Function', 'Thyroid Stimulating Hormone (TSH)'),
('Thyroid Function', 'Free T4 (Thyroxine)'),
('Thyroid Function', 'Free T3 (Triiodothyronine)'),
('Liver Function', 'Liver Function Tests (LFTs)'),
('Liver Function', 'Albumin'),
('Kidney Function', 'Blood Urea Nitrogen (BUN)'),
('Kidney Function', 'Serum Creatinine'),
('Kidney Function', 'Estimated Glomerular Filtration Rate (eGFR)'),
('Infection and Inflammation', 'C-Reactive Protein (CRP)'),
('Infection and Inflammation', 'Erythrocyte Sedimentation Rate (ESR)'),
('Infection and Inflammation', 'Blood Cultures'),
('Nutritional and Vitamin Levels', 'Vitamin D Test'),
('Nutritional and Vitamin Levels', 'Iron Studies'),
('Hormonal Panels', 'Estrogen and Progesterone'),
('Hormonal Panels', 'Testosterone'),
('Hormonal Panels', 'Cortisol'),
('Hormonal Panels', 'Prolactin'),
('Reproductive Health', 'Human Chorionic Gonadotropin (hCG)'),
('Reproductive Health', 'Follicle-Stimulating Hormone (FSH)'),
('Reproductive Health', 'Luteinizing Hormone (LH)'),
('Autoimmune Disorders', 'Antinuclear Antibodies (ANA)'),
('Autoimmune Disorders', 'Rheumatoid Factor (RF)'),
('Allergy Testing', 'IgE Antibody Test'),
('Allergy Testing', 'Skin Prick Test'),
('Cancer Markers', 'Prostate-Specific Antigen (PSA)'),
('Cancer Markers', 'CA-125'),
('Cancer Markers', 'Carcinoembryonic Antigen (CEA)'),
('Genetic Testing', 'BRCA1 and BRCA2'),
('Genetic Testing', 'Carrier Screening'),
('Infectious Diseases', 'HIV Test'),
('Infectious Diseases', 'Hepatitis Panel'),
('Infectious Diseases', 'Tuberculosis (TB) Test'),
('Urine Tests', 'Urinalysis'),
('Urine Tests', 'Urine Culture'),
('Bone Health', 'Bone Mineral Density (BMD) Test'),
('Bone Health', 'Calcium Test'),
('Electrolyte and Fluid Balance', 'Sodium Test'),
('Electrolyte and Fluid Balance', 'Potassium Test'),
('Electrolyte and Fluid Balance', 'Chloride Test'),
('Electrolyte and Fluid Balance', 'Bicarbonate Test'),
('Gastrointestinal Health', 'Helicobacter pylori (H. pylori) Test'),
('Gastrointestinal Health', 'Celiac Disease Panel'),
('Gastrointestinal Health', 'Lactose Intolerance Test'),
('Toxicology and Drug Testing', 'Drug Abuse Panel'),
('Toxicology and Drug Testing', 'Heavy Metals Panel'),
('Toxicology and Drug Testing', 'Alcohol Testing'),
('Immunology and Serology', 'Immunoglobulin Levels (IgA, IgG, IgM)'),
('Immunology and Serology', 'Rubella Antibody Test'),
('Immunology and Serology', 'Hepatitis Serology'),
('Endocrine System', 'Adrenocorticotropic Hormone (ACTH)'),
('Endocrine System', 'Parathyroid Hormone (PTH)'),
('Endocrine System', 'Insulin Test'),
('Rheumatology', 'Anticitrullinated Protein Antibody (ACPA)'),
('Rheumatology', 'Anti-Smith (Anti-Sm) Antibodies'),
('Dermatology', 'Skin Biopsy'),
('Dermatology', 'Patch Testing'),
('Ophthalmology', 'Ocular Pressure Test (Tonometry)'),
('Ophthalmology', 'Retinal Exam'),
('Neurology', 'Electroencephalogram (EEG)'),
('Neurology', 'Nerve Conduction Studies');

