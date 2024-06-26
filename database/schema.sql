CREATE DATABASE medicaldelivery101;

USE medicaldelivery101;
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
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(255) DEFAULT NULL  -- Adding the image_url column with a default value of NULL
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

-- Doctors table
CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    consultation_fee INT NOT NULL,
    doctors_status VARCHAR(255) NOT NULL DEFAULT 'Available',
    doctors_password VARCHAR(255) NOT NULL DEFAULT 12345,
    INDEX idx_name (name) -- Add an index on the name column
);

-- Consultations table
CREATE TABLE consultations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    doctor_id INT NOT NULL,
    doctor_name VARCHAR(100) DEFAULT NULL,
    consultation_date DATE NOT NULL,
    notes TEXT,
    consultation_fee INT NOT NULL,
    consultation_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- Insert sample data into doctors table
INSERT INTO doctors (name, specialty, consultation_fee, doctors_status, doctors_password) VALUES
('Dr. John Smith', 'Cardiology', 150, 'Active', 'password123'),
('Dr. Jane Doe', 'Dermatology', 100, 'Active', 'securepass'),
('Dr. Alice Brown', 'Pediatrics', 120, 'Active', 'letmein'),
('Dr. Ravi Kumar', 'Cardiologist', 500, 'Active', 'password123'),
('Dr. Priya Sharma', 'Dermatologist', 400, 'Active', 'securepass'),
('Dr. Rajesh Singh', 'Pediatrician', 300, 'Active', 'letmein');





INSERT INTO lab_tests (name, description, price) VALUES 
('Basic Health Screening', 'General overview of health status.', 100.00 ),
('Cardiovascular Health', 'Evaluation of heart and blood vessel function.', 150.00),
('Diabetes Management', 'Monitoring and managing blood sugar levels.', 60.00),
('Thyroid Function', 'Assessment of thyroid gland performance.', 80.00),
('Liver Function', 'Analysis of liver enzyme levels.', 60.00),
('Kidney Function', 'Assessment of kidney health.', 65.00),
('Infection and Inflammation', 'Detection of infections and inflammatory conditions.', 50.00),
('Nutritional and Vitamin Levels', 'Measurement of vitamin and nutrient levels.', 90.00),
('Hormonal Panels', 'Assessment of hormone levels in the body.', 110.00),
('Reproductive Health', 'Evaluation of reproductive system health.', 120.00),
('Autoimmune Disorders', 'Detection of autoimmune diseases.', 130.00),
('Allergy Testing', 'Identification of allergic reactions.', 70.00),
('Cancer Markers', 'Screening for cancer indicators.', 200.00),
('Genetic Testing', 'Analysis of genetic predispositions.', 250.00),
('Infectious Diseases', 'Testing for infectious diseases.', 140.00),
('Urine Tests', 'Analysis of urine for various health indicators.', 30.00),
('Bone Health', 'Assessment of bone density and health.', 80.00),
('Electrolyte and Fluid Balance', 'Measurement of electrolyte levels.', 55.00),
('Gastrointestinal Health', 'Evaluation of digestive system health.', 90.00),
('Toxicology and Drug Testing', 'Screening for drugs and toxins.', 100.00),
('Immunology and Serology', 'Assessment of immune system function.', 110.00),
('Endocrine System', 'Evaluation of endocrine gland function.', 120.00),
('Rheumatology', 'Assessment for rheumatic diseases.', 130.00),
('Dermatology', 'Evaluation of skin health.', 70.00),
('Ophthalmology', 'Assessment of eye health.', 90.00),
('Neurology', 'Evaluation of nervous system health.', 150.00);



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


INSERT INTO medicines (name, price, image_url) VALUES
('Paracetamol', 1.00, 'C.jpg'),
('Ibuprofen', 1.50, 'D.jpg'),
('Amoxicillin', 3.00, 'A.jpg'),
('Aspirin', 2.00, 'B.jpg'),
('Cough Syrup', 4.50, 'C.jpg'),
('Antacid', 2.50, 'D.jpg'),
('Vitamin C', 3.00, 'A.jpg'),
('Insulin', 5.00, 'B.jpg'),
('Hydrochlorothiazide', 50.00, 'C.jpg'),
('Prednisone', 70.00, 'D.jpg'),
('Losartan', 55.00, 'A.jpg'),
('Levothyroxine', 65.00, 'B.jpg'),
('Atorvastatin', 80.00, 'C.jpg'),
('Clopidogrel', 45.00, 'D.jpg'),
('Fluoxetine', 90.00, 'A.jpg'),
('Warfarin', 85.00, 'B.jpg'),
('Simvastatin', 75.00, 'C.jpg'),
('Montelukast', 60.00, 'D.jpg'),
('Loratadine', 25.00, 'A.jpg'),
('Metoprolol', 40.00, 'B.jpg'),
('Furosemide', 50.00, 'C.jpg'),
('Gabapentin', 85.00, 'D.jpg'),
('Tramadol', 95.00, 'A.jpg'),
('Citalopram', 70.00, 'B.jpg'),
('Azithromycin', 120.00, 'C.jpg'),
('Doxycycline', 110.00, 'D.jpg'),
('Escitalopram', 105.00, 'A.jpg'),
('Albuterol', 130.00, 'B.jpg');