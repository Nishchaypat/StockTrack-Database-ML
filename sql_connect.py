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


    def insert_portfolio(self, user_id, symbol):
        try:
            self.mycursor.execute("""
                INSERT INTO portfolio(user_id, symbol)
                VALUES(%s, %s);
            """, (user_id, symbol))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        
    def delete_user(self, user_id):
        try:

            self.mycursor.execute("""
                DELETE FROM users WHERE id = %s;
            """, (user_id,))
            self.conn.commit()
            print(f"User with ID {user_id} has been deleted.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def delete_company_from_portfolio(self, user_id, symbol):
        try:

            self.mycursor.execute("""
                DELETE FROM portfolio WHERE user_id = %s AND symbol = %s;
            """, (user_id, symbol))
            self.conn.commit()
            print(f"Company {symbol} has been removed from user {user_id}'s portfolio.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
