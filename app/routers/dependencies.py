from typing import Annotated
from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError 

from services import auth_service



"""
How to define refresh token:

    Create table refresh tokens with 1-1 relationship with user
        user_id = Column(ForeignKey("users.id"), primary_key=True)
        token_hash = Column(String(64), unique=True, nullable=False)
        expires_at = Column(DateTime(timezone=True), nullable=False)
        revoked = Column(Boolean, default=False)
        
        

        
    #2. Login
    Generate jwt token
    Generate refresh token 
    save refresh token hash in db + expirity_date
    set both cookies (when jwt expires , validate the refresh with the one in the db and issue new jwt for (10-15 mins))
    
    #3. Implement Logout
    set revoked=True
    delete both cookies
    
"""

# Extracts Bearer tokens from the Authorization header for Swagger UI without blocking cookie-based fallback auth.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/sessions", auto_error=False)


#def get_home_page(request: Request)
def get_current_user(
    header_token: Annotated[str | None, Depends(oauth2_scheme)] = None,
    cookie_token: Annotated[str | None, Cookie(alias="access_token")] = None
    ) -> dict | None:
    """Extracts and decodes a JWT from the Bearer header or access_token cookie, returning the user dict or None."""
    
    token = header_token or cookie_token
    
    try:
        payload = auth_service.decode_access_token(token)
        
    except ExpiredSignatureError: # if this happens redirect user to the refresh endpoint and back to where he was
        #TODO: refactor to raise custom exception AccessTokenExpired
        return False 
        
    except InvalidTokenError: # Unathorized
        #TODO: refactor to raise custom exception InvalidAccessToken
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