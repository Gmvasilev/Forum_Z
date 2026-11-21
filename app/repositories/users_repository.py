from data.database import (
    read_query,
    insert_query,
    update_query,
    delete_query,
    start_transaction
)

from datetime import datetime
from exceptions.database_validation_error import DatabaseValidationError


def register_full_user_profile(main_data, details_data, update_data):
    
    with start_transaction() as connection:
        
        user_id = insert_query("INSERT INTO table_one...", main_data, connection)
        
        full_details = (user_id,) + details_data
        insert_query("INSERT INTO table_two...", full_details, connection)
        # second_table_params = (generated_id,) + second_table_data[1]
        
        is_updated = update_query("UPDATE table_three...", update_data, connection)
        
        if not is_updated:
            raise DatabaseValidationError("Critical profile update step failed.")
            
    return user_id



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