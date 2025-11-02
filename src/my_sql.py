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

def get_update_query(ids_lenght: int) -> str:
    format_strings = ','.join(['%s'] * ids_lenght)
    concat_photo_url = f"CONCAT('https://{config.BUCKET_NAME}.s3.{config.AWS_REGION}.amazonaws.com/{config.BUCKET_DIR}', id, '.jpg')"
    query = f"UPDATE users SET foto = {concat_photo_url} WHERE id IN ({format_strings})"
    return query

def execute_update_query(ids: set[int]):
    
    with get_mysql_connection() as conn:
        cursor = conn.cursor()
        query = get_update_query(len(ids))
        cursor.execute(query, params=tuple(ids))
        conn.commit()
        cursor.close()
        print(f"Updated photo column for {cursor.rowcount} users.")


    