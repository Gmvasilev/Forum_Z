"""API router for users — register, login, and get current user."""

from fastapi import (
    APIRouter,
    status,
    Cookie,
    Request,
    Depends,
    HTTPException
)

from typing import Annotated
from models.user_models import UserRegister
from routers.dependencies import get_current_user
from app.models.user_models import UserLogin, UserOut
from services import users_service


users_api_router = APIRouter(prefix="/api/users", tags=["Users"])


UNATHORIZED_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired session"
)

# # On registration
# hashed_pw = hash_password(user_in.password.get_secret_value())

# # On login
# is_valid = verify_password(
#     login_in.password.get_secret_value(),
#     user_from_db.hashed_password,
# )



# --- Show certain user Topics & Replies
@users_api_router.get("/{username}")
def 


# ---------------------------------------------------------------------------
# -- USER CRUD operations
# ---------------------------------------------------------------------------


# --- Create User ---
@users_api_router.post("", status_code=status.HTTP_201_CREATED)
def register(new_user: UserRegister):
    pass

# --- Search by username, email, or first name 
@users_api_router.get("", response_model=list[UserOut])
def all_users():
    """
    Not Authenticated: see top 10 users + like/dislike ratio
    Authorized: see all users sorted
    Admin: able to search
    """
    
    # unathorized users can see top 10 users 
    # check_for authorization (admin) -> Unathorized 
    # check for authentication , add query params(username, email, first name (default None))
    pass

# --- Read current user
@users_api_router.get("/me", response_model= UserOut)
def get_current_user_info():
    # check for authentication -> Unathorized
    pass
  
# -- Update User Data ---
@users_api_router.patch("/me")
def update_current_user_data():
    pass

# -- Change User Password --
@users_api_router.put("/me/password")
def change_current_user_password():
    # check for authentication -> Unathorized
    pass


@users_api_router.delete("/me")
def delete_current_user():
    # check for authentication -> Unathorized
    pass

    
    
    
    
# ---------------------------------------------------------------------------
# -- ADMIN operations
# ---------------------------------------------------------------------------

# -- Delete User --
@users_api_router.delete("/{user_id}")
def delete_user():
    
    # check for admin rights
    # soft delete user











@users_api_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate):
    """Register a new user account."""
    try:
        return register_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@users_api_router.post("/login", response_model=Token)
def login(login_data: UserLogin):
    """Authenticate and return a JWT access token."""
    try:
        return login_user(login_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@users_api_router.post("/verify-token", response_model=dict)
def verify_token_endpoint(token: str):
    """Verify a JWT access token and return the embedded username."""
    try:
        token_data = verify_token(token)
        return {"username": token_data.username, "valid": True}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@users_api_router.get("/me", response_model=dict)
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get the currently authenticated user's info (requires Bearer token)."""
    return current_user
