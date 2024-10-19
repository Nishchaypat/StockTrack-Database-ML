import sys
from sql_connect import sql_connector
import re

class StockTrack:

    def __init__(self):
        self.db = sql_connector() 
        self.menu()

    def menu(self):
        user_input = int(input("""
                1. Enter 1 to register\n
                2. Enter 2 to login \n"""))

        if user_input == 1:
            self.register()
        elif user_input == 2:
            self.login()
        else:
            sys.exit(1000)

    def register(self):
        while True:
            firstname = input("Enter your First Name: \n").strip()
            if len(firstname) == 0:
                print("First name cannot be empty. Please enter your first name.")
            else:
                break

        while True:
            lastname = input("Enter your Last Name: \n").strip()
            if len(lastname) == 0:
                print("Last name cannot be empty. Please enter your last name.")
            else:
                break

        while True:
            email = input("Enter your email address: \n").strip()
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Invalid email format. Please try again.")
            else:
                break

        while True:
            password = input("Create your password: \n")
            confirm_password = input("Confirm your password: \n")

            if password != confirm_password:
                print("Passwords do not match. Please try again.")
            elif len(password) < 8:
                print("Password must be at least 8 characters long.")
            elif not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
                print("Password must contain both letters and numbers.")
            else:
                break

        response = self.db.register(firstname, lastname, password, email)

        if response:
            print("Registration successful.")
        else:
            print("Error occurred during registration.")

    def login(self):
        pass

st = StockTrack()
