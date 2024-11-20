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

    def drop_foreign_keys(self):
        # SQL queries to drop foreign key constraints
        drop_foreign_key_stock_prices = """
        ALTER TABLE stock_prices DROP FOREIGN KEY stock_prices_ibfk_1;
        """
        drop_foreign_key_financial_metrics = """
        ALTER TABLE financial_metrics DROP FOREIGN KEY financial_metrics_ibfk_1;
        """
        drop_foreign_key_news_articles = """
        ALTER TABLE news_articles DROP FOREIGN KEY news_articles_ibfk_1;
        """
        try:
            # Execute the drop foreign key queries
            self.mycursor.execute(drop_foreign_key_stock_prices)
            self.mycursor.execute(drop_foreign_key_financial_metrics)
            self.mycursor.execute(drop_foreign_key_news_articles)

            # Commit changes to the database
            self.conn.commit()
            print("Foreign key constraints dropped successfully.")
        except Exception as e:
            print(f"Error dropping foreign key constraints: {e}")

    def drop_tables(self):
        # SQL queries to drop existing tables if they exist
        drop_companies_table = "DROP TABLE IF EXISTS companies;"
        drop_stock_prices_table = "DROP TABLE IF EXISTS stock_prices;"
        drop_financial_metrics_table = "DROP TABLE IF EXISTS financial_metrics;"
        drop_news_articles_table = "DROP TABLE IF EXISTS news_articles;"
        drop_users_table = "DROP TABLE IF EXISTS users;"

        try:
            # Execute the drop table queries
            self.mycursor.execute(drop_companies_table)
            self.mycursor.execute(drop_stock_prices_table)
            self.mycursor.execute(drop_financial_metrics_table)
            self.mycursor.execute(drop_news_articles_table)
            self.mycursor.execute(drop_users_table)

            # Commit changes to the database
            self.conn.commit()
            print("All tables dropped successfully.")
        except Exception as e:
            print(f"Error dropping tables: {e}")

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
    
    # Drop foreign key constraints first
    stock_db.drop_foreign_keys()
    
    # Drop existing tables
    stock_db.drop_tables()

    # Now create new tables
    stock_db.create_tables()
