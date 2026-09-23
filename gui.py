import tkinter as tk
from tkinter import messagebox
import sqlite3

def view_slots_gui():
    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM laundry_slots")
    slots = cursor.fetchall()

    connection.close()

    window = tk.Toplevel()
    window.title("Available Laundry Slots")
    window.geometry("500x400")

    tk.Label(
        window,
        text="Available Laundry Slots",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    if slots:
        for slot in slots:
            text = (
                "Slot ID: " + str(slot[0]) +
                "\nDate: " + slot[1] +
                "\nTime: " + slot[2] +
                "\nCapacity: " + str(slot[3]) +
                "\n----------------------"
            )

            tk.Label(
                window,
                text=text,
                font=("Arial", 11),
                justify="left"
            ).pack(pady=5)

    else:
        tk.Label(
            window,
            text="No laundry slots available."
        ).pack(pady=20)

def book_slot_gui():
    window = tk.Toplevel()
    window.title("Book Laundry Slot")
    window.geometry("400x300")

    tk.Label(
        window,
        text="Book Laundry Slot",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(window, text="Student ID").pack()

    student_id_entry = tk.Entry(window)
    student_id_entry.pack(pady=5)

    tk.Label(window, text="Slot ID").pack()

    slot_id_entry = tk.Entry(window)
    slot_id_entry.pack(pady=5)

    def book():
        student_id = student_id_entry.get()
        slot_id = slot_id_entry.get()

        connection = sqlite3.connect("laundry.db")
        cursor = connection.cursor()

        # Check if student exists
        cursor.execute("""
        SELECT * FROM students
        WHERE student_id = ?
        """, (student_id,))

        student = cursor.fetchone()

        if not student:
            messagebox.showerror(
                "Error",
                "Student ID not found."
            )
            connection.close()
            return

        # Check if slot exists
        cursor.execute("""
        SELECT * FROM laundry_slots
        WHERE slot_id = ?
        """, (slot_id,))

        slot = cursor.fetchone()

        if not slot:
            messagebox.showerror(
                "Error",
                "Slot ID not found."
            )
            connection.close()
            return

        # Check duplicate booking
        cursor.execute("""
        SELECT * FROM bookings
        WHERE student_id = ? AND slot_id = ? AND status = ?
        """, (student_id, slot_id, "Booked"))

        existing_booking = cursor.fetchone()

        if existing_booking:
            messagebox.showerror(
                "Error",
                "You have already booked this slot."
            )
            connection.close()
            return

        # Check capacity
        cursor.execute("""
        SELECT COUNT(*) FROM bookings
        WHERE slot_id = ? AND status = ?
        """, (slot_id, "Booked"))

        current_bookings = cursor.fetchone()[0]
        capacity = slot[3]

        if current_bookings >= capacity:
            messagebox.showerror(
                "Error",
                "This laundry slot is full."
            )
            connection.close()
            return

        # Create booking
        cursor.execute("""
        INSERT INTO bookings (student_id, slot_id, status)
        VALUES (?, ?, ?)
        """, (student_id, slot_id, "Booked"))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Laundry slot booked successfully!"
        )

        window.destroy()

    tk.Button(
        window,
        text="Book Slot",
        command=book,
        width=15
    ).pack(pady=20)

def view_bookings_gui(student_id):
    window = tk.Toplevel()
    window.title("My Bookings")
    window.geometry("500x400")

    tk.Label(
        window,
        text="My Laundry Bookings",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT bookings.booking_id,
           laundry_slots.date,
           laundry_slots.time,
           bookings.status
    FROM bookings
    JOIN laundry_slots
    ON bookings.slot_id = laundry_slots.slot_id
    WHERE bookings.student_id = ?
    """, (student_id,))

    bookings = cursor.fetchall()
    connection.close()

    if bookings:
        for booking in bookings:
            text = (
                "Booking ID: " + str(booking[0]) +
                "\nDate: " + booking[1] +
                "\nTime: " + booking[2] +
                "\nStatus: " + booking[3] +
                "\n----------------------"
            )

            tk.Label(
                window,
                text=text,
                font=("Arial", 11),
                justify="left"
            ).pack(pady=5)

    else:
        tk.Label(
            window,
            text="No bookings found."
        ).pack(pady=20)

def cancel_booking_gui(student_id):
    window = tk.Toplevel()
    window.title("Cancel Booking")
    window.geometry("400x300")

    tk.Label(
        window,
        text="Cancel Laundry Booking",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Enter Booking ID"
    ).pack()

    booking_id_entry = tk.Entry(window)
    booking_id_entry.pack(pady=5)

    def cancel():
        booking_id = booking_id_entry.get()

        connection = sqlite3.connect("laundry.db")
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM bookings
        WHERE booking_id = ?
        AND student_id = ?
        AND status = ?
        """, (booking_id, student_id, "Booked"))

        booking = cursor.fetchone()

        if booking:
            cursor.execute("""
            UPDATE bookings
            SET status = ?
            WHERE booking_id = ?
            """, ("Cancelled", booking_id))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Booking cancelled successfully!"
            )

            window.destroy()

        else:
            connection.close()

            messagebox.showerror(
                "Error",
                "Booking not found or you are not allowed to cancel it."
            )

    tk.Button(
        window,
        text="Cancel Booking",
        command=cancel,
        width=18
    ).pack(pady=20)

def submit_complaint_gui(student_id):
    window = tk.Toplevel()
    window.title("Submit Complaint")
    window.geometry("500x350")

    tk.Label(
        window,
        text="Submit Complaint",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Enter your complaint:"
    ).pack()

    complaint_entry = tk.Text(
        window,
        height=8,
        width=45
    )
    complaint_entry.pack(pady=10)

    def submit():
        complaint = complaint_entry.get("1.0", tk.END).strip()

        if complaint == "":
            messagebox.showerror(
                "Error",
                "Complaint cannot be empty."
            )
            return

        connection = sqlite3.connect("laundry.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO complaints (student_id, complaint, status)
        VALUES (?, ?, ?)
        """, (student_id, complaint, "Pending"))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Complaint submitted successfully!"
        )

        window.destroy()

    tk.Button(
        window,
        text="Submit Complaint",
        command=submit,
        width=18
    ).pack(pady=10)

def view_complaints_gui(student_id):
    window = tk.Toplevel()
    window.title("My Complaints")
    window.geometry("550x450")

    tk.Label(
        window,
        text="My Complaints",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT complaint_id, complaint, status
    FROM complaints
    WHERE student_id = ?
    """, (student_id,))

    complaints = cursor.fetchall()
    connection.close()

    if complaints:
        for complaint in complaints:
            text = (
                "Complaint ID: " + str(complaint[0]) +
                "\nComplaint: " + complaint[1] +
                "\nStatus: " + complaint[2] +
                "\n----------------------"
            )

            tk.Label(
                window,
                text=text,
                font=("Arial", 11),
                justify="left",
                wraplength=450
            ).pack(pady=8)

    else:
        tk.Label(
            window,
            text="No complaints found."
        ).pack(pady=20)

def student_dashboard(student_id):
    dashboard = tk.Toplevel()
    dashboard.title("Student Dashboard")
    dashboard.geometry("500x500")

    tk.Label(
        dashboard,
        text="Student Dashboard",
        font=("Arial", 22, "bold")
    ).pack(pady=30)

    tk.Label(
        dashboard,
        text="Welcome, Student " + str(student_id),
        font=("Arial", 12)
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="View Laundry Slots",
        width=25,
        command=view_slots_gui
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="Book Laundry Slot",
        width=25,
        command=book_slot_gui
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="View Bookings",
        width=25,
        command=lambda: view_bookings_gui(student_id)
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="Cancel Booking",
        width=25,
        command=lambda: cancel_booking_gui(student_id)
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="Submit Complaint",
        width=25,
        command=lambda: submit_complaint_gui(student_id)
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="View Complaints",
        width=25,
        command=lambda: view_complaints_gui(student_id)
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="Logout",
        width=25,
        command=dashboard.destroy
    ).pack(pady=15)
    window = tk.Toplevel()
    window.title("Student Login")
    window.geometry("400x300")

    tk.Label(
        window,
        text="Student Login",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(window, text="Student ID").pack()
    student_id_entry = tk.Entry(window)
    student_id_entry.pack(pady=5)

    tk.Label(window, text="Password").pack()
    password_entry = tk.Entry(window, show="*")
    password_entry.pack(pady=5)

    def login():
        student_id = student_id_entry.get()
        password = password_entry.get()

        connection = sqlite3.connect("laundry.db")
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM students
        WHERE student_id = ? AND password = ?
        """, (student_id, password))

        student = cursor.fetchone()

        connection.close()

        if student:
            messagebox.showinfo("Login", "Login successful!")
            window.destroy()
            student_dashboard(student_id)
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid student ID or password."
            )

    tk.Button(
        window,
        text="Login",
        command=login,
        width=15
    ).pack(pady=20)
def student_login_window():
    window = tk.Toplevel()
    window.title("Student Login")
    window.geometry("400x300")

    tk.Label(
        window,
        text="Student Login",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(window, text="Student ID").pack()

    student_id_entry = tk.Entry(window)
    student_id_entry.pack(pady=5)

    tk.Label(window, text="Password").pack()

    password_entry = tk.Entry(window, show="*")
    password_entry.pack(pady=5)

    def login():
        student_id = student_id_entry.get()
        password = password_entry.get()

        connection = sqlite3.connect("laundry.db")
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM students
        WHERE student_id = ? AND password = ?
        """, (student_id, password))

        student = cursor.fetchone()

        connection.close()

        if student:
            messagebox.showinfo("Login", "Login successful!")
            window.destroy()
            student_dashboard(student_id)
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid student ID or password."
            )

    tk.Button(
        window,
        text="Login",
        command=login,
        width=15
    ).pack(pady=20)

def view_students_gui():
    window = tk.Toplevel()
    window.title("All Students")
    window.geometry("500x400")

    tk.Label(
        window,
        text="Registered Students",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT student_id, name
    FROM students
    """)

    students = cursor.fetchall()
    connection.close()

    if students:
        for student in students:
            text = (
                "Student ID: " + str(student[0]) +
                "\nName: " + student[1] +
                "\n----------------------"
            )

            tk.Label(
                window,
                text=text,
                font=("Arial", 11),
                justify="left"
            ).pack(pady=5)

    else:
        tk.Label(
            window,
            text="No students registered."
        ).pack(pady=20)

def view_all_bookings_gui():
    window = tk.Toplevel()
    window.title("All Bookings")
    window.geometry("600x450")

    tk.Label(
        window,
        text="All Laundry Bookings",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT bookings.booking_id,
           bookings.student_id,
           laundry_slots.date,
           laundry_slots.time,
           bookings.status
    FROM bookings
    JOIN laundry_slots
    ON bookings.slot_id = laundry_slots.slot_id
    """)

    bookings = cursor.fetchall()
    connection.close()

    if bookings:
        for booking in bookings:
            text = (
                "Booking ID: " + str(booking[0]) +
                "\nStudent ID: " + str(booking[1]) +
                "\nDate: " + booking[2] +
                "\nTime: " + booking[3] +
                "\nStatus: " + booking[4] +
                "\n----------------------"
            )

            tk.Label(
                window,
                text=text,
                font=("Arial", 11),
                justify="left"
            ).pack(pady=5)

    else:
        tk.Label(
            window,
            text="No bookings found."
        ).pack(pady=20)

def view_all_complaints_gui():
    window = tk.Toplevel()
    window.title("All Complaints")
    window.geometry("600x450")

    tk.Label(
        window,
        text="All Student Complaints",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    connection = sqlite3.connect("laundry.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT complaint_id, student_id, complaint, status
    FROM complaints
    """)

    complaints = cursor.fetchall()
    connection.close()

    if complaints:
        for complaint in complaints:
            text = (
                "Complaint ID: " + str(complaint[0]) +
                "\nStudent ID: " + str(complaint[1]) +
                "\nComplaint: " + complaint[2] +
                "\nStatus: " + complaint[3] +
                "\n----------------------"
            )

            tk.Label(
                window,
                text=text,
                font=("Arial", 11),
                justify="left",
                wraplength=500
            ).pack(pady=8)

    else:
        tk.Label(
            window,
            text="No complaints found."
        ).pack(pady=20)

def update_complaint_status_gui():
    window = tk.Toplevel()
    window.title("Update Complaint Status")
    window.geometry("450x300")

    tk.Label(
        window,
        text="Update Complaint Status",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Complaint ID"
    ).pack()

    complaint_id_entry = tk.Entry(window)
    complaint_id_entry.pack(pady=5)

    tk.Label(
        window,
        text="New Status"
    ).pack()

    status_entry = tk.Entry(window)
    status_entry.pack(pady=5)

    def update_status():
        complaint_id = complaint_id_entry.get().strip()
        new_status = status_entry.get().strip()

        if complaint_id == "":
            messagebox.showerror(
                "Error",
                "Complaint ID cannot be empty."
            )
            return

        if new_status == "":
            messagebox.showerror(
                "Error",
                "Status cannot be empty."
            )
            return

        connection = sqlite3.connect("laundry.db")
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE complaints
        SET status = ?
        WHERE complaint_id = ?
        """, (new_status, complaint_id))

        connection.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo(
                "Success",
                "Complaint status updated successfully!"
            )
            connection.close()
            window.destroy()
        else:
            connection.close()
            messagebox.showerror(
                "Error",
                "Complaint ID not found."
            )

    tk.Button(
        window,
        text="Update Status",
        command=update_status,
        width=18
    ).pack(pady=20)

def add_laundry_slot_gui():
    window = tk.Toplevel()
    window.title("Add Laundry Slot")
    window.geometry("450x400")

    tk.Label(
        window,
        text="Add Laundry Slot",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Date (DD-MM-YYYY)"
    ).pack()

    date_entry = tk.Entry(window)
    date_entry.pack(pady=5)

    tk.Label(
        window,
        text="Time"
    ).pack()

    time_entry = tk.Entry(window)
    time_entry.pack(pady=5)

    tk.Label(
        window,
        text="Capacity"
    ).pack()

    capacity_entry = tk.Entry(window)
    capacity_entry.pack(pady=5)

    def add_slot():
        date = date_entry.get().strip()
        time = time_entry.get().strip()
        capacity = capacity_entry.get().strip()

        if date == "":
            messagebox.showerror(
                "Error",
                "Date cannot be empty."
            )
            return

        if time == "":
            messagebox.showerror(
                "Error",
                "Time cannot be empty."
            )
            return

        try:
            capacity = int(capacity)

            if capacity <= 0:
                messagebox.showerror(
                    "Error",
                    "Capacity must be greater than 0."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Error",
                "Capacity must be a valid number."
            )
            return

        connection = sqlite3.connect("laundry.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO laundry_slots (date, time, capacity)
        VALUES (?, ?, ?)
        """, (date, time, capacity))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Laundry slot added successfully!"
        )

        window.destroy()

    tk.Button(
        window,
        text="Add Slot",
        command=add_slot,
        width=18
    ).pack(pady=25)

def admin_dashboard():
    dashboard = tk.Toplevel()
    dashboard.title("Admin Dashboard")
    dashboard.geometry("500x500")

    tk.Label(
        dashboard,
        text="Admin Dashboard",
        font=("Arial", 22, "bold")
    ).pack(pady=30)

    tk.Label(
        dashboard,
        text="Welcome, Admin",
        font=("Arial", 12)
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="View Students",
        width=25,
        command=view_students_gui
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="View All Bookings",
        width=25,
        command=view_all_bookings_gui
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="View All Complaints",
        width=25,
        command=view_all_complaints_gui
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="Update Complaint Status",
        width=25,
        command=update_complaint_status_gui
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="Add Laundry Slot",
        width=25,
        command=add_laundry_slot_gui
    ).pack(pady=8)

    tk.Button(
        dashboard,
        text="Logout",
        width=25,
        command=dashboard.destroy
    ).pack(pady=15)


def admin_login_window():
    window = tk.Toplevel()
    window.title("Admin Login")
    window.geometry("400x300")

    tk.Label(
        window,
        text="Admin Login",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Label(window, text="Username").pack()
    username_entry = tk.Entry(window)
    username_entry.pack(pady=5)

    tk.Label(window, text="Password").pack()
    password_entry = tk.Entry(window, show="*")
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "admin123":
            messagebox.showinfo("Login", "Admin login successful!")
            window.destroy()
            admin_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid admin username or password."
            )

    tk.Button(
        window,
        text="Login",
        command=login,
        width=15
    ).pack(pady=20)


# Main window
root = tk.Tk()
root.title("Hostel Laundry Management System")
root.geometry("500x400")

tk.Label(
    root,
    text="HOSTEL LAUNDRY",
    font=("Arial", 24, "bold")
).pack(pady=(50, 5))

tk.Label(
    root,
    text="MANAGEMENT SYSTEM",
    font=("Arial", 18)
).pack(pady=5)

tk.Label(
    root,
    text="Welcome!",
    font=("Arial", 12)
).pack(pady=20)

tk.Button(
    root,
    text="Student Login",
    command=student_login_window,
    width=20
).pack(pady=10)

tk.Button(
    root,
    text="Admin Login",
    command=admin_login_window,
    width=20
).pack(pady=10)

tk.Button(
    root,
    text="Exit",
    command=root.destroy,
    width=20
).pack(pady=10)

root.mainloop()