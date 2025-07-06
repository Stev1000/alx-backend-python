import mysql.connector

def stream_user_ages():
    """
    Generator that connects to ALX_prodev database and yields user ages one by one.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # replace with your MySQL password
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row['age']

    cursor.close()
    conn.close()


def calculate_average_age():
    """
    Uses stream_user_ages generator to compute average age
    without loading all ages into memory at once.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
        return

    average_age = total_age / count
    print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    calculate_average_age()
