import sqlite3
from datetime import datetime
def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == "admin" and password == "admin123":
        print("Admin login successful!")
        admin_menu()
        return True
    else:
        print("Invalid admin username or password.")
        return False


def add_laundry_slot():
    date = input("Enter laundry date (DD-MM-YYYY): ")

    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date. Please use DD-MM-YYYY format.")
        return

    time = input("Enter laundry time: ")

    if time.strip() == "":
        print("Laundry time cannot be empty.")
        return

    try:
        capacity = int(input("Enter slot capacity: "))

        if capacity <= 0:
            print("Capacity must be greater than 0.")
            return

    except ValueError:
        print("Please enter a valid number for capacity.")
        return

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO laundry_slots (date, time, capacity)
    VALUES (?, ?, ?)
    """, (date, time, capacity))

    connection.commit()
    connection.close()

    print("Laundry slot added successfully!")

def update_complaint_status():
    complaint_id = input("Enter the complaint ID: ")
    new_status = input("Enter new status: ")

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE complaints
    SET status = ?
    WHERE complaint_id = ?
    """, (new_status, complaint_id))

    connection.commit()

    if cursor.rowcount > 0:
        print("Complaint status updated successfully!")
    else:
        print("Complaint ID not found.")

    connection.close()

def view_students():
    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    if students:
        print("\nRegistered Students:")
        for student in students:
            print("Student ID:", student[0])
            print("Name:", student[1])
            print("----------------------")
    else:
        print("No students registered.")

    connection.close()

def view_all_bookings():
    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM bookings")

    bookings = cursor.fetchall()

    if bookings:
        print("\nAll Laundry Bookings:")
        for booking in bookings:
            print("Booking ID:", booking[0])
            print("Student ID:", booking[1])
            print("Slot ID:", booking[2])
            print("Status:", booking[3])
            print("----------------------")
    else:
        print("No bookings found.")

    connection.close()

def view_all_complaints():
    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM complaints")

    complaints = cursor.fetchall()

    if complaints:
        print("\nAll Complaints:")
        for complaint in complaints:
            print("Complaint ID:", complaint[0])
            print("Student ID:", complaint[1])
            print("Complaint:", complaint[2])
            print("Status:", complaint[3])
            print("----------------------")
    else:
        print("No complaints found.")

    connection.close()

def admin_menu():
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. View Students")
        print("2. View All Bookings")
        print("3. View All Complaints")
        print("4. Update Complaint Status")
        print("5. Add Laundry Slot")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_students()

        elif choice == "2":
            view_all_bookings()

        elif choice == "3":
            view_all_complaints()

        elif choice == "4":
            update_complaint_status()

        elif choice == "5":
            add_laundry_slot()

        elif choice == "6":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")


