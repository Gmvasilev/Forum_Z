# from typing import Annotated                                        # TODO : remove soon
# from fastapi import Depends, Cookie, Request, Response              # TODO : remove soon


# from fastapi.security import OAuth2PasswordBearer                   # TODO : remove soon
# from jwt.exceptions import InvalidTokenError,ExpiredSignatureError  # TODO : remove soon

from fastapi import Request, Response
from services import auth_service
from exceptions import auth_errors
from config import settings



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

def authenticate(
    request: Request,
    response: Response
) -> dict | None:
    """Returns user_payload on success or None.
    Attaches new acces_token when expired"""
    
    # -- Look for access_token --
    access_token = request.cookies.get("access_token")
    if access_token is None:
        return None
    
    try:
        user_data = auth_service.decode_access_token(access_token)
        
    except auth_errors.AccessTokenExpiredError:
        
        # -- Look for refresh_token --
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token is None:
            return None
        
        # -- Extract payload from expired token
        # -- Catch corrupted signature
        # (jwt checks signature after expiration time)
        try:
            user_data = auth_service.extract_payload_from_expired_token(access_token)
        except auth_errors.AccessTokenInvalidError:
            return None                             
        
        # data for the same user freshly fetched from the db
        synced_user_data  = auth_service.validate_refresh_token(user_data, refresh_token)
        
        new_access_token = auth_service.create_access_token(synced_user_data)
        
        # -- Attach new access_token 
        response.set_cookie(
            key="access_token",
            value = new_access_token,
            httponly=True,
            samesite="lax",
            max_age=settings.access_token_expire_minutes
        )
        
        return synced_user_data
        
    except auth_errors.AccessTokenInvalidError:
        return None

    return user_data
        

    
# #def get_home_page(request: Request)
# def get_current_user_from_jwt(token: str) -> dict | None:
#     """Extracts and decodes a JWT from the Bearer header or access_token cookie, returning the user dict or None."""
    
#     try:
#         payload = auth_service.decode_access_token(token)
        
#     except ExpiredSignatureError: # if this happens redirect user to the refresh endpoint and back to where he was
#         #TODO: refactor to raise custom exception AccessTokenExpired
#         # TODO : skip redirect to refresh and issues new acces token
        
#         return False 
        
#     except InvalidTokenError: # Unathorized
#         #TODO: refactor to raise custom exception InvalidAccessToken
#         return None
    
#     sub: str | None = payload.get("sub")
#     username: str | None = payload.get("username")
#     role: str | None = payload.get("role")
    
#     if sub is None or username is None or role is None:
#         return None
        
#     try:
#         user_id = int(sub)
#     except ValueError:
#         return None
    
#     return {
#         "user_id": user_id,
#         "username": username,
#         "role": role
#     }
    
    
    
    
# # API router
# def extract_access_token_from_header(
#     header_token: Annotated[str | None, Depends(oauth2_scheme)] = None
# ) -> str | None:
#     return header_token


# # WEB router
# def extract_access_token_from_cookie(
#     cookie_token: Annotated[str | None, Cookie(alias="access_token")] = None
# ) -> str | None:
#     return cookie_token
    