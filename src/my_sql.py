import mysql.connector
import config
from contextlib import contextmanager
from sshtunnel import SSHTunnelForwarder

@contextmanager
def get_mysql_connection():
    try:

        if not config.shoud_use_ssh_tunnel():
            connection = mysql.connector.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME
            )
            yield connection
        else:
            with SSHTunnelForwarder(
                ssh_address_or_host=(config.SSH_HOST, config.SSH_PORT),
                ssh_username=config.SSH_USER,
                ssh_pkey=config.SSH_KEY_PATH,
                remote_bind_address=(config.DB_HOST, config.DB_PORT),
                local_bind_address=('127.0.0.1', 0)
            ) as tunnel:
                connection = mysql.connector.connect(
                    host="127.0.0.1",
                    port=tunnel.local_bind_port,
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


    