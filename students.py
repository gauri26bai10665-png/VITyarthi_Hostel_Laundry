import sqlite3


def register_student():
    name = input("Enter your name: ")
    student_id = input("Enter your student ID: ")
    password = input("Create a password: ")

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
        INSERT INTO students (student_id, name, password)
        VALUES (?, ?, ?)
        """, (student_id, name, password))

        connection.commit()
        print("Registration successful!")

    except sqlite3.IntegrityError:
        print("This student ID is already registered.")

    connection.close()


def login_student():
    student_id = input("Enter your student ID: ")
    password = input("Enter your password: ")

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id = ? AND password = ?
    """, (student_id, password))

    student = cursor.fetchone()

    if student:
        print("Login successful!")
        print("Welcome,", student[1])
        student_menu()
    else:
        print("Invalid student ID or password.")

    connection.close()

def view_slots():
    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM laundry_slots
    """)

    slots = cursor.fetchall()

    if slots:
        print("\nAvailable Laundry Slots:")
        for slot in slots:
            print("Slot ID:", slot[0])
            print("Date:", slot[1])
            print("Time:", slot[2])
            print("Capacity:", slot[3])
            print("----------------------")
    else:
        print("No laundry slots available.")

    connection.close()

def book_slot():
    student_id = input("Enter your student ID: ")
    slot_id = input("Enter the slot ID you want to book: ")

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    # Check if student exists
    cursor.execute("""
    SELECT * FROM students
    WHERE student_id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if not student:
        print("Student ID not found. Please register first.")
        connection.close()
        return

    # Check if the slot exists
    cursor.execute("""
    SELECT * FROM laundry_slots
    WHERE slot_id = ?
    """, (slot_id,))

    slot = cursor.fetchone()

    if not slot:
        print("Slot ID not found.")
        connection.close()
        return

    # Check if the student already booked this slot
    cursor.execute("""
    SELECT * FROM bookings
    WHERE student_id = ? AND slot_id = ? AND status = ?
    """, (student_id, slot_id, "Booked"))

    existing_booking = cursor.fetchone()

    if existing_booking:
        print("You have already booked this slot.")
        connection.close()
        return

    # Check slot capacity
    cursor.execute("""
    SELECT COUNT(*) FROM bookings
    WHERE slot_id = ? AND status = ?
    """, (slot_id, "Booked"))

    current_bookings = cursor.fetchone()[0]
    capacity = slot[3]

    if current_bookings >= capacity:
        print("This laundry slot is full.")
        connection.close()
        return

    # Create booking
    cursor.execute("""
    INSERT INTO bookings (student_id, slot_id, status)
    VALUES (?, ?, ?)
    """, (student_id, slot_id, "Booked"))

    connection.commit()
    connection.close()

    print("Laundry slot booked successfully!")

    # Check if the student already has an active booking
    cursor.execute("""
    SELECT * FROM bookings
    WHERE student_id = ? AND slot_id = ? AND status = ?
    """, (student_id, slot_id, "Booked"))

    existing_booking = cursor.fetchone()

    if existing_booking:
        print("You have already booked this slot.")
        connection.close()
        return
        # Check slot capacity
    cursor.execute("""
    SELECT COUNT(*) FROM bookings
    WHERE slot_id = ? AND status = ?
    """, (slot_id, "Booked"))

    current_bookings = cursor.fetchone()[0]

    capacity = slot[3]

    if current_bookings >= capacity:
        print("This laundry slot is full.")
        connection.close()
        return
    
        # Create the booking
    cursor.execute("""
    INSERT INTO bookings (student_id, slot_id, status)
    VALUES (?, ?, ?)
    """, (student_id, slot_id, "Booked"))

    connection.commit()
    connection.close()

    print("Laundry slot booked successfully!")

def view_bookings():
    student_id = input("Enter your student ID: ")

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM bookings
    WHERE student_id = ?
    """, (student_id,))

    bookings = cursor.fetchall()

    if bookings:
        print("\nYour Bookings:")
        for booking in bookings:
            print("Booking ID:", booking[0])
            print("Student ID:", booking[1])
            print("Slot ID:", booking[2])
            print("Status:", booking[3])
            print("----------------------")
    else:
        print("No bookings found.")

    connection.close()

def cancel_booking():
    student_id = input("Enter your student ID: ")
    booking_id = input("Enter the booking ID you want to cancel: ")

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM bookings
    WHERE booking_id = ? AND student_id = ? AND status = ?
    """, (booking_id, student_id, "Booked"))

    booking = cursor.fetchone()

    if booking:
        cursor.execute("""
        UPDATE bookings
        SET status = ?
        WHERE booking_id = ?
        """, ("Cancelled", booking_id))

        connection.commit()
        print("Booking cancelled successfully!")
    else:
        print("Booking not found or you are not allowed to cancel it.")

    connection.close()

def view_complaints():
    student_id = input("Enter your student ID: ")

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM complaints
    WHERE student_id = ?
    """, (student_id,))

    complaints = cursor.fetchall()

    if complaints:
        print("\nYour Complaints:")
        for complaint in complaints:
            print("Complaint ID:", complaint[0])
            print("Student ID:", complaint[1])
            print("Complaint:", complaint[2])
            print("Status:", complaint[3])
            print("----------------------")
    else:
        print("No complaints found.")

    connection.close()

def submit_complaint():
    student_id = input("Enter your student ID: ")
    complaint = input("Enter your complaint: ")

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO complaints (student_id, complaint, status)
    VALUES (?, ?, ?)
    """, (student_id, complaint, "Pending"))

    connection.commit()
    connection.close()

    print("Complaint submitted successfully!")
    
def student_menu():
    while True:
        print("\n===== STUDENT MENU =====")
        print("1. View Laundry Slots")
        print("2. Book Laundry Slot")
        print("3. View Bookings")
        print("4. Cancel Booking")
        print("5. Submit Complaint")
        print("6. View Complaints")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_slots()

        elif choice == "2":
            book_slot()

        elif choice == "3":
            view_bookings()

        elif choice == "4":
            cancel_booking()

        elif choice == "5":
            submit_complaint()

        elif choice == "6":
            view_complaints()

        elif choice == "7":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")


