# TODO: MariaDB connection / pool
import re
from mariadb import connect, Error
from mariadb.connections import Connection
from app.config import settings
from exceptions.database_validation_error import DatabaseValidationError


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

def update_query(sql:str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount > 0

def delete_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount > 0
    
    
def insert_one_to_one_records(
    main_table_data: tuple[str, tuple],
    second_table_data: tuple[str, tuple]
):
    """Insert two records into a 1:1 relationship as a single atomic transaction.\n
    Second table will have the generated id from the first table added as its first param\n
    Params:
        tuple contains a SQL query string and a tuple of its parameteres"""
        
    with _get_connection() as conn:
        conn.autocommit = False
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                main_table_data[0],
                main_table_data[1])
            
            generated_id = cursor.lastrowid
            
            second_table_params = (generated_id,) + second_table_data[1]

            cursor.execute(
                second_table_data[0],
                second_table_params
            )
            
            conn.commit()
            
        except Error as e:
            
            conn.rollback()
            
            user_msg = _parse_mariadb_error(e)
            
            raise DatabaseValidationError(user_msg)
        

def atomic_batch(
    operations: list[tuple[str, tuple]],
    enforce_affected_rows: bool = False
):
    
    """Execute a collection of SQL commands (INSERT, UPDATE, DELETE) in one transaction.\n

    Commits all changes if every query succeeds, or rolls back the entire batch\n
    if any single query fails or (optionally) affects zero rows.
    
    Params:
        operations: List of tuples containing the SQL string and its parameters.
        enforce_affected_rows: If True, raises an error if any query affects 0 rows.
    Returns:
        int: The total number of rows affected by all queries combined.

    Raises:
        DatabaseValidationError: If a unique/check constraint is violated or 
        no rows were affected when enforced.
    """

    with _get_connection() as conn:
        
        conn.auto_reconnect = False
        cursor = conn.cursor()
        
        try:
            for sql,data in operations:
                cursor.execute(sql, data)
                
                if enforce_affected_rows and cursor.rowcount == 0:
                    # trigger rollback
                    raise DatabaseValidationError("Any of the queries didnt affect any rows.")
                
            conn.commit()
        except Error as e:
            conn.rollback()
            user_friendly_msg = _parse_mariadb_error(e)
            raise DatabaseValidationError(user_friendly_msg) from e
            
            
    
    
def _parse_mariadb_error(e: Error) -> str:
    """
    Parses MariaDB constraints by scanning the error text directly for 
    known technical prefixes, extracting only the underlying column name.
    """
    error_text = e.errmsg

    # 1. UNIQUE Violations (Error 1062)
    if e.errno == 1062:
        # Search word starting with 'uq_' (ex: 'uq_username' or 'uq_email')
        match = re.search(r"\b(uq_[a-zA-Z0-9_]+)\b", error_text)
        if match:
            # Extract constraint name (removing table name if present)
            constraint_name = match.group(1).split('.')[-1]
            # Remove 'uq_' from start
            column_name = re.sub(r'^uq_', '', constraint_name)
            return f"The {column_name} is already taken."
        
        return "A unique constraint validation failed."

    # 2. CHECK Violations (Error 4025)
    elif e.errno == 4025:
        # Searching word starting with 'chck_' (ex: chck_firstname_length')
        match = re.search(r"\b(chck_[a-zA-Z0-9_]+)\b", error_text)
        if match:
            constraint_name = match.group(1)
            # Remov 'chck_' from start
            column_name = re.sub(r'^chck_', '', constraint_name)
            
            # Remove '_length' from end:
            clean_column = re.sub(r'_length$', '', column_name)
            
            return f"The value provided for {clean_column} does not meet the requirements."
        
        return "A data constraint validation failed."

    return f"A database error occurred (Code: {e.errno})."