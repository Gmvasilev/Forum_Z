
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Response
from fastapi.security import OAuth2PasswordRequestForm
from models.user_models import UserLogin
from services import auth_service
from services.auth_service import REFRESH_TOKEN_LIFETIME_IN_SECONDS


auth_api_router = APIRouter(prefix="/api/sessions", tags=["Authentication"])


UNATHORIZED_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired session"
)



# -- Login --
@auth_api_router.post("", response_model=dict)
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
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_LIFETIME_IN_SECONDS,
        path= "/api/sessions/current" # send the cookie only when this is the path
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
    
# -- Refresh Auth Token
@auth_api_router.post("/current", response_model = str)
def refresh_access_token(
    refresh_token: Annotated[str | None, Cookie()] = None
):
    """Refresh the current authentication session."""
    
    if refresh_token is None:
        raise UNATHORIZED_HTTP_EXCEPTION
    
    access_token = auth_service.refresh(refresh_token)
    
    if access_token is None:
        raise UNATHORIZED_HTTP_EXCEPTION
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
        }

    
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


