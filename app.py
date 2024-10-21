import sys
from sql_connect import sql_connector
import re

class StockTrack:

    def __init__(self):
        self.db = sql_connector() 
        self.user_id = None
        self.menu()

    def menu(self):
        while True:  
            user_input = int(input("""
                1. Enter 1 to register\n
                2. Enter 2 to login \n
                3. Enter 3 to insert a company \n
                4. Enter 4 to delete a company \n
                5. Enter 5 to delete your account \n
                6. Enter 6 to exit\n"""))

            if user_input == 1:
                self.register()
            elif user_input == 2:
                self.login()
            elif user_input == 3:
                if self.user_id:
                    ticker = input("Add your company ticker: ").strip()
                    self.portfolio(ticker)
                else:
                    print("Please log in first.")
            elif user_input == 4:
                self.delete_company()
            elif user_input == 5:
                self.delete_user()
            elif user_input == 6:
                print("Exiting application.")
                sys.exit(0)
            else:
                print("Invalid option. Please choose again.")

    def register(self):
        while True:
            firstname = input("Enter your First Name: \n").strip()
            if not firstname:
                print("First name cannot be empty.")
            else:
                break

        while True:
            lastname = input("Enter your Last Name: \n").strip()
            if not lastname:
                print("Last name cannot be empty.")
            else:
                break

        while True:
            email = input("Enter your email address: \n").strip()
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Invalid email format.")
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

        response = self.db.register(firstname, lastname, email, password)

        if response:
            print("Registration successful.")
        else:
            print("Error occurred during registration.")

    def login(self):
        email = input("Enter your email address: \n")
        password = input("Enter your password: \n")
        response = self.db.search(email, password)

        if response:
            print("Login successful.")
            self.user_id = int(response[0][0]) 
        else:
            print("Login failed. Please check your credentials.")

    def portfolio(self, ticker):

        response = self.db.insert_portfolio(self.user_id, ticker)
        if response:
            print(f"Company {ticker} added to your portfolio.")
        else:
            print(f"Error occurred while adding {ticker} to portfolio.")

    def delete_user(self):
        confirm = input("Are you sure you want to delete your account? Y - Yes | N - No")
        if confirm == 'Y':
            self.db.delete_user(self.user_id)
        
    def delete_company(self):
        ticker = input("Enter the company ticker that you want to delete: ")
        self.db.delete_company_from_portfolio(self.user_id, ticker)


if __name__ == "__main__":
    st = StockTrack()

