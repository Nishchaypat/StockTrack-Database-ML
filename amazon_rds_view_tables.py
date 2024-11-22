import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="database-1.cds0coo26frf.us-east-1.rds.amazonaws.com",
    user="adminstocktrack",
    password="Nrp212300",
    port=3306,
    database="stocktrack"
)

# Create a cursor
cursor = conn.cursor()

# Show tables in the database
cursor.execute("SHOW TABLES")

# Fetch all table names
tables = cursor.fetchall()

# Iterate through tables and display content
for (table_name,) in tables:
    print(f"\nContent of table: {table_name}")
    cursor.execute(f"SELECT * FROM {table_name}")  # Limit to 10 rows for readability
    rows = cursor.fetchall()
    
    # Print column headers
    column_names = [desc[0] for desc in cursor.description]
    print(" | ".join(column_names))
    
    # Print each row
    for row in rows:
        print(" | ".join(str(item) for item in row))

# Close the connection
cursor.close()
conn.close()
