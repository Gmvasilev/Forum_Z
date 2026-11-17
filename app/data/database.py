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