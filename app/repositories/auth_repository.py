from data.database import (
    read_query,
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
    
    
def validate_refresh_token(refresh_token_hash: str, current_time: datetime) -> tuple | None:
    """Returns the user(id, username, role) if the token is valid, else None"""
    
    res = read_query(
        """
        SELECT
            u.user_id,
            u.username,
            u_r.user_role
        FROM
            refresh_tokens r_t
        JOIN
            users u ON r_t.user_id = u.user_id
        JOIN
            user_roles u_r ON u.user_role_id = u_r.user_role_id
        WHERE
            token_hash = ? 
        AND expires_at > ?
        AND is_revoked = FALSE
        """,
        (refresh_token_hash, current_time, )
    )
    
    return res[0] or None
    
    
    