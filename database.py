import sqlite3

connection = sqlite3.connect("laundry.db")

cursor = connection.cursor()

# Students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Laundry slots table
cursor.execute("""
CREATE TABLE IF NOT EXISTS laundry_slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    capacity INTEGER NOT NULL
)
""")

# Bookings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    slot_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (slot_id) REFERENCES laundry_slots(slot_id)
)
""")

# Complaints table
cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    complaint TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
""")
connection.commit()

print("Database tables created successfully!")

connection.close()