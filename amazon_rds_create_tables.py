import mysql.connector
import bcrypt
import sys

class stockdata():
    def __init__(self):
        try:
            # Connect to the Amazon RDS MySQL instance
            self.conn = mysql.connector.connect(
                host="database-1.cds0coo26frf.us-east-1.rds.amazonaws.com",
                user="adminstocktrack",
                password="Nrp212300",
                port=3306,
                database="stocktrack"
            )
            self.mycursor = self.conn.cursor()
        except Exception as e:
            print("Some error occurred:", e)
            sys.exit(0)

    def create_tables(self):
        # SQL queries to create necessary tables if they don't already exist
        create_companies_table = """
        CREATE TABLE IF NOT EXISTS companies (
            symbol VARCHAR(10) NOT NULL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            sector VARCHAR(255),
            industry VARCHAR(255),
            description TEXT
        );
        """
        
        create_stock_prices_table = """
        CREATE TABLE IF NOT EXISTS stock_prices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            open_price FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume INT,
            FOREIGN KEY (symbol) REFERENCES companies(symbol)
        );
        """
        
        create_financial_metrics_table = """
        CREATE TABLE IF NOT EXISTS financial_metrics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            quarter DATE NOT NULL,
            revenue FLOAT,
            earnings FLOAT,
            dividends FLOAT,
            FOREIGN KEY (symbol) REFERENCES companies(symbol)
        );
        """
        
        create_news_articles_table = """
        CREATE TABLE IF NOT EXISTS news_articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            title VARCHAR(255),
            content TEXT,
            published_date DATETIME,
            FOREIGN KEY (symbol) REFERENCES companies(symbol)
        );
        """

        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            firstname VARCHAR(255),
            lastname VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        );
        """

        try:
            # Execute the table creation queries
            self.mycursor.execute(create_companies_table)
            self.mycursor.execute(create_stock_prices_table)
            self.mycursor.execute(create_financial_metrics_table)
            self.mycursor.execute(create_news_articles_table)
            self.mycursor.execute(create_users_table)
            
            # Commit changes to the database
            self.conn.commit()
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")

if __name__ == "__main__":
    stock_db = stockdata()
    stock_db.create_tables()
