import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows from user_data table
    in batches of size batch_size.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # replace with your MySQL password
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return

    cursor = conn.cursor(dictionary=True)

    offset = 0
    while True:
        cursor.execute(
            "SELECT * FROM user_data ORDER BY user_id LIMIT %s OFFSET %s",
            (batch_size, offset)
        )
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """
    Processes each batch of users, filtering only those over age 25,
    and yields them one by one.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
