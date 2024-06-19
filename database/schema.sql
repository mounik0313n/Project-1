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

-- Doctors table
CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL
);

-- Consultations table
CREATE TABLE consultations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    doctor_id INT NOT NULL,
    consultation_date DATE NOT NULL,
    notes TEXT,
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