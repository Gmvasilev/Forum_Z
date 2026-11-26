
"""Password hashing and JWT token utilities."""

from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
import jwt.exceptions as jwt_exceptions
import base64
import hashlib
import secrets
from typing import Any

from config import settings
from repositories import users_repository, auth_repository
from exceptions import auth_errors




def login(username: str, password: str) -> tuple[str, str] | None:
    """ Returns tuple(jwt_token, refresh_token) or None on fail"""
    
    user_data = users_repository.get_user_by_username(username)
    
    if user_data is None:
        return None
    
    user_id, username, password_hash, user_role = user_data
    
    if not _verify_password(password, password_hash):
        return None
    
    jwt_payload = _generate_jwt_payload(user_id, username, user_role)
    
    jwt_token = create_access_token(jwt_payload) 
    refresh_token = _create_refresh_token()
    
    # save token hash in db
    refresh_token_hash = _hash_refresh_token(refresh_token)
    expires = _generate_token_expiration_date(
        timedelta(seconds=settings.refresh_token_expire_secconds)
    )
    
    auth_repository.activate_refresh_token(
        user_id,
        refresh_token_hash,
        expires
    )

    return (jwt_token, refresh_token)


def validate_refresh_token(user_id: int, refresh_token):
    """Validate refresh token and return fresh user data from the db."""
    
    hashed_refresh_token = _hash_refresh_token(refresh_token)
    current_time = _generate_token_expiration_date(timedelta(0))
    
    res = auth_repository.validate_refresh_token(user_id, hashed_refresh_token, current_time)
    
    if res is None:
        return None
    
    return _generate_jwt_payload(*res)
    

# def refresh(user_id: int, refresh_token: str) -> str | None:
#     """Validate a refresh token and return a new access JWT.
#     Or None."""
    
#     hashed_refresh_token = _hash_refresh_token(refresh_token)
#     # add 2 minutes as if the renovation happened 2 minutes later
#     current_time = _generate_token_expiration_date(timedelta(minutes=2))
    
#     res = auth_repository.validate_refresh_token(user_id, hashed_refresh_token, current_time)
    
#     if res is None:
#         return None
    
#     return create_access_token(
#         _generate_jwt_payload(*res)
#     )


#------------------------------------------------
# -- JWT token ----------------------------------
#------------------------------------------------

def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token.\n
    Raises AccessTokenExpiredError if token expired\n
    Raises InvalidTokenError if token invalid.\n
    Returns tokens payload."""

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
    except jwt_exceptions.ExpiredSignatureError:
        raise auth_errors.AccessTokenExpiredError("JWT access token expired!")
    except jwt_exceptions.InvalidTokenError:
        raise auth_errors.AccessTokenInvalidError("Received JWT is corrupted or forged!")
        
    return payload


def extract_payload_from_expired_token(token: str) -> dict:
    """Extract payload from an EXPIRED JWT access token.\n
    Ignores expiration, but strictly validates the signature and structure.\n
    Raises AccessTokenInvalidError if the token is corrupted or forged.\n
    Returns tokens payload.
    """
    
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"verify_exp": False} # skip time check
        )
    except jwt_exceptions.InvalidTokenError:
        raise auth_errors.AccessTokenInvalidError("Received JWT is corrupted or forged!")
    
    return payload
    
    
def create_access_token(payload_data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token with the given payload data.\n
    If expires_delta is ommited fallsback to .env - ACCESS_TOKEN_EXPIRE_MINUTES"""
    
    to_encode = payload_data.copy()
    
    if expires_delta is not None:
        expire = _generate_token_expiration_date(expires_delta)
    else:
        expire = _generate_token_expiration_date(
            timedelta(minutes=settings.access_token_expire_minutes)
        )
        
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return encoded_jwt

def _generate_jwt_payload(user_id: int, username: str, user_role: str) -> dict[str, Any]:
    """Provide a single, discoverable place to define and review JWT claims."""
    
    return {
        "sub": user_id, 
        "username": username,
        "role": user_role
    }



#------------------------------------------------
# -- Refresh token ------------------------------
#------------------------------------------------

def _create_refresh_token() -> str:
    """Generate a cryptographically secure random refresh token."""
    
    return secrets.token_urlsafe(32)


def _hash_refresh_token(token: str) -> str:
    """Return the SHA-256 hash used to store and identify refresh tokens."""
    
    return hashlib.sha256(token.encode("utf-8")).hexdigest()



#------------------------------------------------
# -- Tokens Common ------------------------------
#------------------------------------------------

def _generate_token_expiration_date(time: timedelta) -> datetime:
    """Calculate the future UTC expiration datetime using a positive time offset."""
    return datetime.now(timezone.utc) + time



#-------------------------------------------------
# -- Password ------------------------------------
#-------------------------------------------------

def hash_password(password: str) -> str:
    """Hash a string password using SHA-256 pre-hashing and bcrypt."""
    
    prepared = _prepare_password(password)
    salt = bcrypt.gensalt() # salt is contained in the hash
    hashed = bcrypt.hashpw(prepared, salt)
    return hashed.decode("utf-8")


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    
    prepared = _prepare_password(plain_password)
    return bcrypt.checkpw(
        prepared, hashed_password.encode("utf-8")
    )


def _prepare_password(password: str) -> bytes:
    """Return a Base64-encoded SHA-256 digest suitable for bcrypt."""
    
    raw_bytes = password.encode("utf-8") # convert password to bytes
    digest = hashlib.sha256(raw_bytes).digest() # generate 256 bits / 8 = 32 raw bytes
    return base64.b64encode(digest) # re-pack by 6 = 44 safe charecters


    

    









#TODO put public methods on top after coding
#hash_pas, decode, login, logout, refresh


    

# def logout(refresh_token: str):
    
#     hashed_refresh_token = _hash_refresh_token(refresh_token)
    
    
#     # 2. Find the refresh-token record by hash. extract[user_id, username, role, expires_at, revoked]
#     #    If not found, return None.
#     # 3. Check expiration and revocation.
#     #    If invalid, return None.
#     # 4. Retrieve the associated user.
#     #    If not found, return None.
#     # 5. Generate a new JWT using the user's claims.
#     # 6. Return the new access JWT.
    
#     #TODO: set revoked=True in refresh_tokens table for the matching hashed_refresh_token
    
    

# def decode_access_token(token: str) -> dict:
#     """Decode and validate a JWT access token. Raises HTTPException if invalid."""
#     try:
#         payload = jwt.decode(
#             token, settings.secret_key, algorithms=[settings.algorithm]
#         )
#         return payload
    
#     except InvalidTokenError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials", # schupihte tokena hakeri
#             headers={"WWW-Authenticate": "Bearer"},
#         )   

# #def get_home_page(request: Request)
# def get_current_user(
#     header_token: Annotated[str | None, Depends(oauth2_scheme)] = None,
#     cookie_token: Annotated[str | None, Cookie(alias="access_token")] = None
#     ) -> dict | None:
#     """Extracts and decodes a JWT from the Bearer header or access_token cookie, returning the user dict or None."""

#     token = header_token or cookie_token
    
#     payload = decode_access_token(token)
#     username: str = payload.get("sub")
#     if username is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
        
#     # TODO:
#     #userid
#     #userrole
#     return {"username": username}






