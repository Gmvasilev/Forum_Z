# TODO: MariaDB connection / pool
import re
from enum import Enum
from contextlib import contextmanager, nullcontext
from mariadb import Connection, connect, Error


from config import settings
from exceptions.database_errors import DatabaseValidationError


class QueryMode(Enum):
    FETCH = "fetch"
    LASTROWID = "lastrowid"
    ROWCOUNT = "rowcount"


def _get_connection() -> Connection:
    
    return connect(
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name
    )
    
    
def _execute(
    sql: str,
    sql_params: tuple,
    connection: Connection | None,
    mode: QueryMode
):
    """
    Execute a SQL statement and return a result based on the given mode.
    FETCH -> list of row tuples, LASTROWID -> generated id, ROWCOUNT -> bool.
    If no connection is provided, opens one and auto-commits.
    """
    
    connection_provider = (
        _get_connection()
        if connection is None
        else nullcontext(connection) # nullcontext wraps the connecion taking the hit from the current with block end
    )                                # the connection is safely closed from start_stransaction()
    
    with connection_provider as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, sql_params)

            if connection is None and mode != QueryMode.FETCH:
                conn.commit()
                
            if mode == QueryMode.FETCH:
                return list(cursor)
            elif mode == QueryMode.LASTROWID:
                return cursor.lastrowid
            elif mode == QueryMode.ROWCOUNT:
                return cursor.rowcount > 0
            return cursor
        
        except Error as e:
            
            user_friendly_msg = _parse_mariadb_error(e)
            raise DatabaseValidationError(user_friendly_msg) from e
    
        finally:
            cursor.close()
    


def read_query(sql, sql_params=(), connection=None) -> list[tuple]:
    """Returns all matching rows as a list of tuples."""
    
    return _execute(sql, sql_params, connection, QueryMode.FETCH)


def insert_query(sql, sql_params=(), connection=None) -> int:
    """Returns the generated primary key id."""
    
    return _execute(sql, sql_params, connection, QueryMode.LASTROWID)


def update_query(sql, sql_params=(), connection=None) -> bool:
    """Returns True if at least one row was affected."""
    
    return _execute(sql, sql_params, connection,  QueryMode.ROWCOUNT)


def delete_query(sql, sql_params=(), connection=None) -> bool:
    """Returns True if at least one row was affected."""
    
    return _execute(sql, sql_params, connection, QueryMode.ROWCOUNT)

def exists_query(sql, sql_params=(), connection=None) -> bool:
    """Returns True if the record exists, False otherwise."""
    result = _execute(sql, sql_params, connection, QueryMode.FETCH)
    
    # no result 
    if not result or not result[0]:
        return False
        
    # for SELECT EXISTS queries
    return bool(result[0][0])

    
@contextmanager
def start_transaction():
    """
    Open an atomic database transaction using a context manager.
    
    Must be invoked using a 'with' block. Automatically commits 
    on success or rolls back on any exception.
    
    Yields:
        mariadb.Connection: The active transactional connection session.
    """
    with _get_connection() as conn:
        conn.autocommit = False # Must be set before any statement executes
        try:
            yield conn  # Hand over the connection to the'with' block
            # EVERYTHING BELOW EXECUTES AFTER THE CALLER WITH BLOCK FINISHES
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    

def _parse_mariadb_error(e: Error) -> str:
    """
    Parse MariaDB exceptions and translate strict constraint violations 
    into clean, user-friendly messages.
    """
    # Safe extraction of error attributes
    error_text = e.errmsg if hasattr(e, 'errmsg') else str(e)
    error_code = e.errno if hasattr(e, 'errno') else None

    # 1. UNIQUE CONSTRAINT VIOLATION (e.g., uq_username, uq_email)
    if error_code == 1062:
        # Scan for any word boundary starting with 'uq_' prefix
        match = re.search(r"\b(uq_[a-zA-Z0-9_]+)\b", error_text)
        if match:
            # Drop table prefix if present, then strip the 'uq_' prefix
            constraint_name = match.group(1).split('.')[-1]
            column_name = re.sub(r'^uq_', '', constraint_name)
            return f"The {column_name} is already taken."
        return "A unique constraint validation failed."

    # 2. CHECK CONSTRAINT VIOLATION (e.g., chck_firstname_length)
    elif error_code == 4025:
        # Scan for any word boundary starting with 'chck_' prefix
        match = re.search(r"\b(chck_[a-zA-Z0-9_]+)\b", error_text)
        if match:
            constraint_name = match.group(1)
            column_name = re.sub(r'^chck_', '', constraint_name)
            # Remove common suffix to isolate the pure column name
            clean_column = re.sub(r'_length$', '', column_name)
            return f"The value provided for {clean_column} is invalid."
        return "A database check constraint validation failed."

    # 3. FOREIGN KEY VIOLATION (Relational data integrity locks)
    elif error_code in (1216, 1217, 1451, 1452):
        if "delete" in error_text.lower() or "update" in error_text.lower():
            return "This record cannot be modified or deleted as it is linked to other data."
        return "The referenced parent record does not exist."

    # 4. INFRASTRUCTURE & CRITICAL DATABASE CRASHES
    elif error_code in (2002, 2003, 2006, 2013):
        return "The database server is currently unavailable. Please try again later."

    # 5. GLOBAL FALLBACK FOR UNHANDLED ERRORS
    return "A database error occurred. Please contact support."




#! KEEPING THIS JUNK UNTIL I have everything replacing it tested

#! OLD QUERIES
# def read_query(sql: str, sql_params=(), connection: Connection=None) -> list[tuple]:
#     """ Returns list of table rows as tuples"""
    
#     connection_provider = (
#         _get_connection()
#         if connection is None
#         else nullcontext(connection) # nullcontext wraps the connecion taking the hit from the current with block end
#     )                                # the connection is safely closed from start_stransaction()
    
#     with connection_provider as conn:
#         try:
#             cursor = conn.cursor()
#             cursor.execute(sql, sql_params)

#             return list(cursor)
        
#         except Error as e:
#             user_friendly_msg = _parse_mariadb_error(e)
#             raise DatabaseValidationError(user_friendly_msg) from e
    
#         finally:
#             cursor.close()


# def insert_query(sql: str, sql_params=(), connection: Connection=None) -> int:
#     """ Returns the last row generated id."""
    
#     connection_provider = (
#         _get_connection()
#         if connection is None
#         else nullcontext(connection) # nullcontext wraps the connecion taking the hit from the current with block end
#     )                                # the connection is safely closed from start_stransaction()
    
#     with connection_provider as conn:
#         try:
#             cursor = conn.cursor()
#             cursor.execute(sql, sql_params)
        
#             if connection is None:
#                 conn.commit()

#             return cursor.lastrowid
        
#         except Error as e:
#             user_friendly_msg = _parse_mariadb_error(e)
#             raise DatabaseValidationError(user_friendly_msg) from e
        
#         finally:
#             cursor.close()


# def update_query(sql:str, sql_params=(), conection: Connection=None) -> bool:
#     """ Returns any row affected ?"""
    
#     connection_provider = (
#         _get_connection()
#         if conection is None
#         else nullcontext(conection) # nullcontext wraps the connecion taking the hit from the current with block end
#     )                               # the connection is safely closed from start_stransaction()
    
#     with connection_provider as conn:
#         try:
#             cursor = conn.cursor()
#             cursor.execute(sql, sql_params)
            
#             if conection is None:
#                 conn.commit()

#             return cursor.rowcount > 0
        
#         except Error as e:
#             user_friendly_msg = _parse_mariadb_error(e)
#             raise DatabaseValidationError(user_friendly_msg) from e
        
#         finally:
#             cursor.close()




# def insert_one_to_one_records(
#     main_table_data: tuple[str, tuple],
#     second_table_data: tuple[str, tuple]
# ):
#     """Insert two records into a 1:1 relationship as a single atomic transaction.\n
#     Second table will have the generated id from the first table added as its first param\n
#     Params:
#         tuple contains a SQL query string and a tuple of its parameteres"""
        
#     with _get_connection() as conn:
#         conn.autocommit = False
#         cursor = conn.cursor()
        
#         try:
#             cursor.execute(
#                 main_table_data[0],
#                 main_table_data[1])
            
#             generated_id = cursor.lastrowid
            
#             second_table_params = (generated_id,) + second_table_data[1]

#             cursor.execute(
#                 second_table_data[0],
#                 second_table_params
#             )
            
#             conn.commit()
            
#         except Error as e:
            
#             conn.rollback()
            
#             user_msg = _parse_mariadb_error(e)
            
#             raise DatabaseValidationError(user_msg)
        

# def atomic_batch(
#     operations: list[tuple[str, tuple]],
#     enforce_affected_rows: bool = False
# ):
    
#     """Execute a collection of SQL commands (INSERT, UPDATE, DELETE) in one transaction.\n

#     Commits all changes if every query succeeds, or rolls back the entire batch\n
#     if any single query fails or (optionally) affects zero rows.
    
#     Params:
#         operations: List of tuples containing the SQL string and its parameters.
#         enforce_affected_rows: If True, raises an error if any query affects 0 rows.
#     Returns:
#         int: The total number of rows affected by all queries combined.

#     Raises:
#         DatabaseValidationError: If a unique/check constraint is violated or 
#         no rows were affected when enforced.
#     """

#     with _get_connection() as conn:
        
#         conn.auto_reconnect = False
#         cursor = conn.cursor()
        
#         try:
#             for sql,data in operations:
#                 cursor.execute(sql, data)
                
#                 if enforce_affected_rows and cursor.rowcount == 0:
#                     # trigger rollback
#                     raise DatabaseValidationError("Any of the queries didnt affect any rows.")
                
#             conn.commit()
#         except Error as e:
#             conn.rollback()
#             user_friendly_msg = _parse_mariadb_error(e)
#             raise DatabaseValidationError(user_friendly_msg) from e
            
            
    