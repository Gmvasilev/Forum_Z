from data.database import (
    read_query,
    insert_query,
    update_query,
    delete_query,
    start_transaction
)

from typing import Any
from exceptions.database_errors import DatabaseValidationError

DEFAULT_USER_ROLE = "user"


def insert(user_data: dict[str, Any]):
    """
    Register a new user and their refresh token atomically.
    user_data keys: first_name, last_name, username, email, password(hash)
    """
    
    with start_transaction() as connection:
        
        # 1. Insert User
        generated_user_id = insert_query(
            """
            INSERT INTO 
                users(
                    first_name,
                    last_name,
                    username,
                    email,
                    password_hash,
                    user_role_id
                )
            VALUES
                (?,?,?,?,?,
                    (SELECT user_role_id FROM user_roles WHERE user_role = ?)
                )
            """, 
            (
                user_data["first_name"],
                user_data["last_name"],
                user_data["username"],
                user_data["email"],
                user_data["password"],
                DEFAULT_USER_ROLE
            ),
            connection
        )
        
        # 2. Insert refresh token 
        insert_query(
            """
            INSERT INTO
                refresh_tokens(
                    user_id
                )
            VALUES
                (?)
            """,
            (generated_user_id, ),
            connection
        )
 
    return generated_user_id



def get_user_by_username(username: str) -> tuple:
    """Returns (user_id, username, password_hash, user_role)\n
        or None if NOT found."""
    
    user_row = read_query(
        """
        SELECT
            u.user_id,
            u.username,
            u.password_hash,
            u_r.user_role
        FROM
            users u
        JOIN
            user_roles u_r on u.user_role_id = u_r.user_role_id
        WHERE username = ?
        """, 
        (username, )
    )
    
    if not user_row[0]: # No result
        return None
    
    print(user_row)
    
    return user_row[0]
    