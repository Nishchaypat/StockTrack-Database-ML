import sys
from sql_connect import sql_connector
import re
from stock_data import stockdata

class StockTrack:

    def __init__(self):
        self.db = sql_connector() 
        self.menu()

    def menu(self):
        user_input = int(input("""
                1. Enter 1 to register\n
                2. Enter 2 to login \n)
                3. Enter 3 to insert a comapany \n"""))

        if user_input == 1:
            self.register()
        elif user_input == 2:
            self.login()
        elif user_input == 3:
            ticker = str(input("Enter a company ticker"))
            self.company_table(ticker)
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

        response = self.db.register(firstname, lastname, email, password)

        if response:
            print("Registration successful.")
        else:
            print("Error occurred during registration.")

    def login(self):
        email = input("Enter your email address: \n")
        password = input("Enter your password: \n")
        response = self.db.search(email, password)

        print(response)

    def stock_price_table(self, response, ticker):
        company_sd = stockdata(ticker)
        stock_data = company_sd.stockprice(ticker)
        for row in stock_data:
            date = row['Date'] 
            open_price = row['Open']
            high = row['High']
            low = row['Low']
            close = row['Close']
            volume = row['Volume']
            
            self.db.insert_stock_price(response, date, open_price, high, low, close, volume)
        self.financial_metric_table(response, ticker)

    def company_table (self, ticker):
        company_sd = stockdata(ticker)
        
        company_data = company_sd.company()
        response = self.db.insert_company(company_data["Name"], company_data["Sector"], company_data["Industry"], company_data["Description"])
        
        self.stock_price_table(response, ticker)

    def financial_metric_table(self, response, ticker):
        company_sd = stockdata(ticker)
        fin_data = company_sd.finmetric(ticker)
        quarter = fin_data['quarter'] 
        revenue = fin_data['revenue']
        earnings = fin_data['earnings']
        dividends = fin_data['quarter']


        self.db.insert_financial_metric(response, quarter, revenue, earnings, dividends)
        self.news_table(response, ticker)

    def news_table(self, response, ticker):
        company_sd = stockdata(ticker)
        
        stock_news_data = company_sd.news(ticker)

        for row in stock_news_data:
            date = row['published_date'] 
            title = row['title']
            content = row['content']
            
            self.db.insert_news_article(response, title, content, date)

st = StockTrack()
