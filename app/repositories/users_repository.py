# TODO: user repository (raw SQL)


from datetime import datetime


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