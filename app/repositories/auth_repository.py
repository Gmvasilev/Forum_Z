from data.database import (
    update_query,
    exists_query
)

from datetime import datetime


def activate_refresh_token(user_id: int, refresh_token_hash: str, expiration: datetime) -> bool:
    """Returns wheter token singleton associated with user_id was found and updated."""
    
    return update_query(
        """
        UPDATE
            refresh_tokens
        SET
            token_hash = ?,
            expires_at = ?,
            is_revoked = FALSE
        WHERE
            user_id = ?
        """,
        (refresh_token_hash, expiration, user_id)
    )
    

    
def deactivate_refresh_token(refresh_token_hash: str):
    """Returns whether the token(hash) was found and updated."""
    
    return update_query(
        """
        UPDATE
            refresh_tokens
        SET
            is_revoked = TRUE
        WHERE
            token_hash = ?
        """,
        (refresh_token_hash, )
    )
    
    
def validate_refresh_token(refresh_token_hash: str, current_time: datetime) -> bool:
    """Returns that the token was found, not expired, and not revoked"""
    
    return  exists_query(
        """
        SELECT
            1 
        FROM
            refresh_tokens 
        WHERE
            token_hash = ? 
        AND expires_at > ?
        AND is_revoked = FALSE
        """,
        (refresh_token_hash, current_time, )
    )
    
    
    
    