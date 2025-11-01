import mysql.connector
import config
from contextlib import contextmanager

@contextmanager
def get_mysql_connection():

    try:
        connection = mysql.connector.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        yield connection
    except mysql.connector.Error as err:
        print(f"Error opening MySQL connection: {err}")
        yield None
    finally:
        if connection and connection.is_connected():
            connection.close()

def test_connection():
    with get_mysql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT NOW();")
        now = cursor.fetchone()
        cursor.close()
        print("MySQL connected. Database time is:", now[0])