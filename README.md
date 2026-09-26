# Hostel Laundry Management System

## About the Project

The Hostel Laundry Management System is a straightforward application which has been developed as part of the VITyarthi project and is intended to simplify the laundry process for both students and administrators.

Students are able to see the available laundry slots, book and cancel them, make complaints, and check the status of their complaints. The administrator has the capability of managing students, the laundry slots, the bookings, and the complaints.

## Technologies Used

- Python
- Tkinter
- SQLite
- Git and GitHub

## Main Features

### Student Module
- Student login
- View available laundry slots
- Book a laundry slot
- View booking history
- Cancel a booking
- Submit complaints
- View complaint status

### Admin Module
- Admin login
- View registered students
- View all bookings
- View all complaints
- Update complaint status
- Add laundry slots

## Project Structure

The main program flow is managed by `main.py`
- `students.py` holds functions that deal with students
The file `admin.py` includes functions that are related to administration.
- database.py – sets up and handles the SQLite database tables
The file gui.py offers the Tkinter graphical user interface.
The SQLite database called laundry.db is used by the application.
– .gitignore stops Git from tracking unnecessary files

## How the System Works

Students are able to log into the system and use the student dashboard to manage their laundry bookings and complaints. Similarly, administrators can log in on their own and, using the admin dashboard, manage the laundry slots, bookings, students, and complaints.

The application stores student information, laundry slots, bookings, and complaints using SQLite.

## Purpose

This project is mainly intended to offer a simple way of dealing with hostel laundry activities and at the same time to show how Python programming, database management, GUI development, and version control can be used.

## Developed For

**VITyarthi Project**

**Project Title:** Hostel Laundry Management System