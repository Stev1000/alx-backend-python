import time
import sqlite3
import functools

query_cache = {}

# DB connection decorator (reuse from previous task)
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Cache decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get query string (must be passed as keyword or second argument)
        query = kwargs.get('query') if 'query' in kwargs else args[1] if len(args) > 1 else None
        if query in query_cache:
            print("Cache hit. Returning cached result.")
            return query_cache[query]
        print("Cache miss. Executing and caching query.")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call — caches the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call — uses cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
