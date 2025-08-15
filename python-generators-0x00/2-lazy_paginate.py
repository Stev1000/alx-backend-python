#!/usr/bin/python3
seed = __import__('seed')

def paginate_users(page_size, offset):
    """
    Fetch a page of users from user_data table with given page_size and offset.
    Returns a list of user dicts.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator that yields pages of users lazily, one page at a time.
    Stops when no more data.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
