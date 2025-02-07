import mysql.connector
import pandas as pd
conn = mysql.connector.connect(
    host="database-1.cds0coo26frf.us-east-1.rds.amazonaws.com",
    user="adminstocktrack",
    password="Nrp212300",
    port=3306,
    database="stocktrack"
)

mycursor = conn.cursor()

df = pd.read_csv('C:/Users/Nishc/OneDrive - Georgia State University/StockTrack/predicted_new.csv')
print("CSV file read successfully.")
df.drop(columns=['Unnamed: 0'], inplace=True)
# Insert data from the CSV
for index, row in df.iterrows():
    print(f"Inserting row {index}: {row['symbol']}, {row['actual']}, {row['predicted']}, {row['date']}")
    mycursor.execute("""
        INSERT INTO Prediction (symbol, actual, predicted, Date)
        VALUES (%s, %s, %s, %s)
    """, (row['symbol'], row['actual'], row['predicted'], row['date']))

conn.commit()
print("Data inserted successfully.")
mycursor.close()
conn.close()
