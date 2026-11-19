from typing import Annotated
from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from helpers.security import decode_access_token




# Extracts Bearer tokens from the Authorization header for Swagger UI without blocking cookie-based fallback auth.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users", auto_error=False)


#def get_home_page(request: Request)
def get_current_user(
    header_token: Annotated[str | None, Depends(oauth2_scheme)] = None,
    cookie_token: Annotated[str | None, Cookie(alias="access_token")] = None
    ) -> dict | None:
    """Extracts and decodes a JWT from the Bearer header or access_token cookie, returning the user dict or None."""
    
    token = header_token or cookie_token
    try:
        payload = decode_access_token(token)
    except InvalidTokenError:
        return None
    
    sub: str | None = payload.get("sub")
    username: str | None = payload.get("username")
    role: str | None = payload.get("role")
    
    if sub is None or username is None or role is None:
        return None
        
    try:
        user_id = int(sub)
    except ValueError:
        return None
    
    return {
        "user_id": user_id,
        "username": username,
        "role": role
        }