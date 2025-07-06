import mysql.connector

def stream_users():
    """
    Generator function that connects to the ALX_prodev database,
    fetches rows one by one from the user_data table,
    and yields each row as a dictionary.
    """
    try:
        # Connect to the ALX_prodev database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # Replace with your MySQL root password
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return  # Exit generator if connection fails

    cursor = conn.cursor(dictionary=True)  # Get rows as dictionaries

    try:
        cursor.execute("SELECT * FROM user_data")
        # Use a single loop to fetch rows lazily and yield one by one
        for row in cursor:
            yield row
    finally:
        cursor.close()
        conn.close()
