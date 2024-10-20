import sys
import mysql.connector

class sql_connector():
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host="localhost", user="root", password="", database="stocktrack")
            self.mycursor = self.conn.cursor()
        except Exception as e:
            print("Some error occurred:", e)
            sys.exit(0)

    def register(self, firstname, lastname, email, password):
        try:
            self.mycursor.execute("""
                INSERT INTO users (firstname, lastname, email, password) 
                VALUES (%s, %s, %s, %s);
            """, (firstname, lastname, email, password))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def search(self, email, password):
        try:
            self.mycursor.execute("""
                SELECT * FROM users 
                WHERE email = %s AND password = %s;
            """, (email, password))
            data = self.mycursor.fetchall()
            return data
        except Exception as e:
            print(f"Error: {e}")
            return False

    def insert_company(self, name, sector, industry, description):
        try:
            self.mycursor.execute("""
                INSERT INTO company (name, sector, industry, description) 
                VALUES (%s, %s, %s, %s);
            """, (name, sector, industry, description))
            self.conn.commit()
            return self.mycursor.lastrowid 
        except Exception as e:
            print(f"Error: {e}")
            return None

    def insert_stock_price(self, company_id, date, open_price, high, low, close, volume):
        try:
            self.mycursor.execute("""
                INSERT INTO stock_price (company_id, date, open, high, low, close, volume) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (company_id, date, open_price, high, low, close, volume))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def insert_financial_metric(self, company_id, quarter, revenue, earnings, dividends):
        try:
            self.mycursor.execute("""
                INSERT INTO financial_metric (company_id, quarter, revenue, earnings, dividends) 
                VALUES (%s, %s, %s, %s, %s);
            """, (company_id, quarter, revenue, earnings, dividends))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def insert_news_article(self, company_id, title, content, published_date):
        try:
            self.mycursor.execute("""
                INSERT INTO news_article (company_id, title, content, published_date) 
                VALUES (%s, %s, %s, %s);
            """, (company_id, title, content, published_date))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def insert_economic_indicator(self, gdp, inflation_rate, interest_rate, date):
        try:
            self.mycursor.execute("""
                INSERT INTO economic_indicator (gdp, inflation_rate, interest_rate, date) 
                VALUES (%s, %s, %s, %s);
            """, (gdp, inflation_rate, interest_rate, date))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
