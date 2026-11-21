from data.database import (
    read_query,
    insert_query,
    update_query,
    delete_query,
    start_transaction
)

from typing import Any
from datetime import datetime
from exceptions.database_validation_error import DatabaseValidationError

DEFAULT_USER_ROLE = "user"

def insert(user_data: dict[str, Any]):
    """
    Register a new user and their refresh token atomically.
    user_data keys: first_name, last_name, username, email, password_hash
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
                user_data["password_hash"],
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



def get_user_by_username(username: str):
    #TODO return [user_id, username, password_hash,  role]
    
    
    #return None #On failure
    return []

def update_refresh_token(
    user_id: int,
    token_hash: str,
    expires_at: datetime
) -> None:
    """Update the user's refresh token and expiration."""
    pass


def revoke_refresh_token(user_id: int) -> None:
    """Mark the user's refresh token as revoked."""
    pass