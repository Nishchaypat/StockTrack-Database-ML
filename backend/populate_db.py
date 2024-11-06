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
    def insert_company(self, symbol, name, sector, industry, description):
        try:
            self.mycursor.execute("""
                INSERT INTO company (symbol, name, sector, industry, description) 
                VALUES (%s, %s, %s, %s, %s);
            """, (symbol, name, sector, industry, description))
            self.conn.commit()
            return self.mycursor.lastrowid 
        except Exception as e:
            print(f"Error: {e}")
            return None

    def insert_stock_price(self, symbol, date, open_price, high, low, close, volume):
        try:
            self.mycursor.execute("""
                INSERT INTO stock_price (symbol, date, open, high, low, close, volume) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (symbol, date, open_price, high, low, close, volume))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def insert_financial_metric(self, symbol, quarter, revenue, earnings, dividends):
        try:
            self.mycursor.execute("""
                INSERT INTO financial_metric (symbol, quarter, revenue, earnings, dividends) 
                VALUES (%s, %s, %s, %s, %s);
            """, (symbol, quarter, revenue, earnings, dividends))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def insert_news_article(self, symbol, title, content, published_date):
        try:
            self.mycursor.execute("""
                INSERT INTO news_article (symbol, title, content, published_date) 
                VALUES (%s, %s, %s, %s);
            """, (symbol, title, content, published_date))
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
    
    def update_dividends(self, symbol, dividend):
        try:
            self.mycursor.execute("""
                UPDATE financial_metric
                SET dividends = %s
                WHERE symbol = %s;
            """, (dividend, symbol))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        