
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Cookie, Response
from models.user_models import UserLogin
from services import auth_service 


auth_api_router = APIRouter(prefix="/api/sessions", tags=["Authentication"])


UNATHORIZED_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired session"
)



# -- Login --
@auth_api_router.post("", response_model=dict)
def login(
    response: Response,
    user_credentials: UserLogin
):
    
    #user_credentials.

    result = auth_service.login(
        user_credentials.username,
        user_credentials.password
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
        max_age=30 * 24 * 60 * 60 # 30 days
    )
    
    response.set_cookie("refresh_token",refresh_token)
    
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
    # check if hash values match with the database 
    # expired ?
    # or revoked ?
    
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
    
    
    # try set the refresh_token to revoked_true
    response.delete_cookie("refresh_token")
    return "Logged out successfully"


