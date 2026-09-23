from students import login_student
from admin import admin_login


print("===== HOSTEL LAUNDRY MANAGEMENT SYSTEM =====")
print("1. Student")
print("2. Admin")
print("3. Exit")

choice = input("Enter your choice: ")

if choice == "1":
    login_student()

elif choice == "2":
    admin_login()

elif choice == "3":
    print("Thank you for using the system!")

else:
    print("Invalid choice.")
