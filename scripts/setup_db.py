import mysql.connector

# Connect to the Docker MySQL instance
db = mysql.connector.connect(
    host="localhost",
    port="3307",
    user="root",
    password="Sum10_slam",
    database="vehicle_parking"
)
cursor = db.cursor()

# Define and execute the schemas individually
table_parking_slots = """
CREATE TABLE IF NOT EXISTS parking_slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slot_number VARCHAR(10),
    status VARCHAR(20) DEFAULT 'available',
    distance_from_entry INT
);
"""
cursor.execute(table_parking_slots)

table_vehicles = """
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20),
    owner_name VARCHAR(50),
    entry_time DATETIME,
    exit_time DATETIME,
    fee_paid DECIMAL(10,2) DEFAULT 0.00,
    vehicle_type VARCHAR(10),
    slot_id INT,
    FOREIGN KEY (slot_id) REFERENCES parking_slots(id)
);
"""
cursor.execute(table_vehicles)

table_receipts = """
CREATE TABLE IF NOT EXISTS receipts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20),
    total_fee DECIMAL(10,2),
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
cursor.execute(table_receipts)

# Insert the initial 10 parking slots if the table is empty
cursor.execute("SELECT COUNT(*) FROM parking_slots")
if cursor.fetchone()[0] == 0:
    cursor.execute("""
        INSERT INTO parking_slots (slot_number, status, distance_from_entry) VALUES
        ('1', 'available', 5), ('2', 'available', 8), ('3', 'available', 12),
        ('4', 'available', 15), ('5', 'available', 18), ('6', 'available', 22),
        ('7', 'available', 25), ('8', 'available', 30), ('9', 'available', 35),
        ('10', 'available', 40)
    """)
    db.commit()

print("Database tables created successfully!")
cursor.close()
db.close()