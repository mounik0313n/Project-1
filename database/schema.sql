create database medicaldelivery1;

use medicaldelivery1;
-- Users table
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

-- Medicines table
CREATE TABLE medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Cart table
CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    medicine_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE CASCADE
);

-- Orders table
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

-- Lab Tests table
CREATE TABLE lab_tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

-- User Lab Tests table
CREATE TABLE user_lab_tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    lab_test_id INT NOT NULL,
    date DATE NOT NULL,
    results TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lab_test_id) REFERENCES lab_tests(id) ON DELETE CASCADE
);



-- Create the doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    consultation_fee INT NOT NULL,
    doctors_status VARCHAR(255) NOT NULL,
    doctors_password VARCHAR(255) NOT NULL
);
ALTER TABLE doctors
ADD COLUMN doctors_status VARCHAR(255) NOT NULL;




-- Insert sample data into doctors table
INSERT INTO doctors (name, specialty, consultation_fee) VALUES 
('Dr. John Smith', 'Cardiology', 150),
('Dr. Jane Doe', 'Dermatology', 100),
('Dr. Alice Brown', 'Pediatrics', 120);


-- Consultations table
CREATE TABLE consultations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    doctor_id INT NOT NULL,
    consultation_date DATE NOT NULL,
    doctor_name varchar,
    notes TEXT,
    consultation_fee INT NOT NULL,
    consultation_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
    FOREIGN KEY (name) REFERENCES doctors(name) ON DELETE CASCADE
);

-- 
CREATE TABLE consultations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    doctor_id INT NOT NULL,
    doctor_name VARCHAR(100) NOT NULL,
    consultation_date DATE NOT NULL,
    notes TEXT,
    consultation_fee INT NOT NULL,
    consultation_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_name) REFERENCES doctors(name) ON DELETE CASCADE
);


DROP table doctors;
INSERT INTO consultations (user_id, doctor_id, consultation_date, notes, consultation_fee, consultation_time)
SELECT 1, id, '2024-06-21', 'Routine check-up', consultation_fee, '10:00:00'
FROM doctors
WHERE id = 1;

select * from doctors;
SHOW TABLES;



INSERT INTO medicines (name, price) VALUES 
('Paracetamol', 1.00),
('Ibuprofen', 1.50),
('Amoxicillin', 3.00),
('Aspirin', 2.00),
('Cough Syrup', 4.50),
('Antacid', 2.50),
('Vitamin C', 3.00),
('Insulin', 5.00); 


INSERT INTO medicines (name, price)
VALUES ('Hydrochlorothiazide', 50.00),
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

       
INSERT INTO doctors (name, specialty) VALUES 
('Dr. John Doe', 'Cardiologist'),
('Dr. Jane Smith', 'Dermatologist'),
('Dr. Emily Johnson', 'General Physician'),
('Dr. Michael Brown', 'Pediatrician'),
('Dr. William Davis', 'Orthopedic Surgeon'),
('Dr. Linda Martinez', 'Gynecologist'); 
select *from doctors;
ALTER TABLE doctors
ADD COLUMN doctor_status VARCHAR(20) NOT NULL DEFAULT 'Available';

ALTER TABLE doctors
MODIFY COLUMN doctor_status VARCHAR(255) NOT NULL DEFAULT 'Available';

ALTER TABLE doctors
MODIFY COLUMN doctors_status VARCHAR(20) DEFAULT 'active';


ALTER TABLE doctors
DROP COLUMN doctors_password;

DROP TABLE consultations;

-- Disable safe update mode
SET SQL_SAFE_UPDATES = 0;

-- Check if the consultation_fee column exists, and add it if it doesn't
ALTER TABLE doctors
ADD COLUMN IF NOT EXISTS consultation_fee INT NOT NULL;

-- Insert sample data into doctors table if not already present
INSERT INTO doctors (name, specialty, consultation_fee)
SELECT * FROM (SELECT 'Dr. John Smith', 'Cardiology', 150) AS tmp
WHERE NOT EXISTS (
    SELECT name FROM doctors WHERE name = 'Dr. John Smith' AND specialty = 'Cardiology' AND consultation_fee = 150
) LIMIT 1;

INSERT INTO doctors (name, specialty, consultation_fee)
SELECT * FROM (SELECT 'Dr. Jane Doe', 'Dermatology', 100) AS tmp
WHERE NOT EXISTS (
    SELECT name FROM doctors WHERE name = 'Dr. Jane Doe' AND specialty = 'Dermatology' AND consultation_fee = 100
) LIMIT 1;

INSERT INTO doctors (name, specialty, consultation_fee)
SELECT * FROM (SELECT 'Dr. Alice Brown', 'Pediatrics', 120) AS tmp
WHERE NOT EXISTS (
    SELECT name FROM doctors WHERE name = 'Dr. Alice Brown' AND specialty = 'Pediatrics' AND consultation_fee = 120
) LIMIT 1;

-- Insert a new consultation using the consultation_fee from the doctors table
INSERT INTO consultations (user_id, doctor_id, consultation_date, notes, consultation_fee, consultation_time)
SELECT 1, id, '2024-06-21', 'Routine check-up', consultation_fee, '10:00:00'
FROM doctors
WHERE id = 1;

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

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    consultation_fee INT NOT NULL,
    doctors_status VARCHAR(255) NOT NULL,
    doctors_password VARCHAR(255) NOT NULL,
    INDEX idx_name (name)  -- Add an index on the name column
);

CREATE TABLE consultations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    doctor_id INT NOT NULL,
    doctor_name VARCHAR(100) NOT NULL,
    consultation_date DATE NOT NULL,
    notes TEXT,
    consultation_fee INT NOT NULL,
    consultation_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_name) REFERENCES doctors(name) ON DELETE CASCADE
);
INSERT INTO doctors (name, specialty, consultation_fee, doctors_status, doctors_password)
VALUES
('Dr. Ravi Kumar', 'Cardiologist', 500, 'Active', 'password123'),
('Dr. Priya Sharma', 'Dermatologist', 400, 'Active', 'securepass'),
('Dr. Rajesh Singh', 'Pediatrician', 300, 'Active', 'letmein');

ALTER TABLE consultations
MODIFY COLUMN doctor_name VARCHAR(100) DEFAULT NULL;