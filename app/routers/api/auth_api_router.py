
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Response
from fastapi.security import OAuth2PasswordRequestForm
from models.user_models import UserLogin
from services import auth_service
from config import settings

auth_api_router = APIRouter(prefix="/api/sessions", tags=["Authentication"])


UNATHORIZED_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired session"
)



# -- Login --
@auth_api_router.post("", status_code=status.HTTP_201_CREATED)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response
):
        
    result = auth_service.login(
        form_data.username,
        form_data.password
    )
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    
    access_token, refresh_token = result
    
    response.set_cookie(
        key="access_token",
        value = access_token,
        httponly=True,
        samesite="lax",
        max_age=settings.access_token_expire_minutes
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=settings.refresh_token_expire_secconds
        # path= "/api/sessions/current" # send the cookie only when this is the path
    )
    
    
    
# -- Refresh Auth Token
# @auth_api_router.post("/current", response_model = str)
# def refresh_access_token(
#     refresh_token: Annotated[str | None, Cookie()] = None
# ):
#     """Refresh the current authentication session."""
    
#     if refresh_token is None:
#         raise UNATHORIZED_HTTP_EXCEPTION
    
#     access_token = auth_service.refresh(refresh_token)
    
#     if access_token is None:
#         raise UNATHORIZED_HTTP_EXCEPTION
    
#     return {
#         "access_token": access_token,
#         "token_type": "bearer"
#         }

    
# -- Logout --
@auth_api_router.delete("/current", response_model=str)
def logout(
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None
):
    """Deletes th"""
    
    # try set the refresh_token to revoked_true
    response.delete_cookie("refresh_token")
    return "Logged out successfully"


