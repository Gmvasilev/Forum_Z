# TODO: MariaDB connection / pool
from mariadb import connect
from mariadb.connections import Connection
from app.config import settings


def _get_connection() -> Connection:
    return connect(
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name
    )

def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)

def insert_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor=conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid

def update_qury(sql:str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit

        cursor.rowcout > 0

def delete_query(sql: str, sql_params=()) -> bool:
    with _get_connection as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcout > 0