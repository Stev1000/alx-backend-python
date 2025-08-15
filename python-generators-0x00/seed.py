import mysql.connector
import csv

# Connect to the MySQL server (not to a specific database)
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"  # Replace with your actual root password
        )
    except mysql.connector.Error as err:
        print(f"Connection Error: {err}")
        return None

# Create the ALX_prodev database if it doesn't exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Database Creation Error: {err}")

# Connect to the ALX_prodev database
def connect_to_prodev():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Connection to ALX_prodev failed: {err}")
        return None

# Create the user_data table
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            );
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Table Creation Error: {err}")

# Insert data from CSV file if not already in the database
def insert_data(connection, file_path):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM user_data;")
        existing_ids = {row[0] for row in cursor.fetchall()}

        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            new_rows = 0
            for row in reader:
                if row['user_id'] not in existing_ids:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (row['user_id'], row['name'], row['email'], row['age']))
                    new_rows += 1

        connection.commit()
        print(f"{new_rows} new rows inserted.")
        cursor.close()
    except Exception as e:
        print(f"Data Insertion Error: {e}")
