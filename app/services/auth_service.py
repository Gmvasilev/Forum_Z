
"""Password hashing and JWT token utilities."""

from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
import base64
import hashlib
import secrets
from typing import Any+

from app.config import settings
import repositories.users_repository as u_repo


def _create_refresh_token() -> str:
    """Generate a cryptographically secure random refresh token."""
    
    return secrets.token_urlsafe(32)


def _hash_refresh_token(token: str) -> str:
    """Return the SHA-256 hash used to store and identify refresh tokens."""
    
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _prepare_password(password: str) -> bytes:
    """Return a Base64-encoded SHA-256 digest suitable for bcrypt."""
    
    raw_bytes = password.encode("utf-8") # convert password to bytes
    digest = hashlib.sha256(raw_bytes).digest() # generate 256 bits / 8 = 32 raw bytes
    return base64.b64encode(digest) # re-pack by 6 = 44 safe charecters


def _hash_password(password: str) -> str:
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


def _generate_jwt_payload(user_id: int, username: str, user_role: str) -> dict[str, Any]:
    """Provide a single, discoverable place to define and review JWT claims."""
    
    return {
        "sub": user_id, 
        "username": username,
        "role": user_role
    }


def _create_access_token(payload_data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token with the given payload data.\n
    If expires_delta is ommited fallsback to .env - ACCESS_TOKEN_EXPIRE_MINUTES"""
    
    to_encode = payload_data.copy()
    
    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token. Raises InvalidTokenError if invalid."""

    payload = jwt.decode(
        token, settings.secret_key, algorithms=[settings.algorithm]
    )
    
    return payload


#TODO put public methods on top after coding
def login(username: str, password: str) -> tuple[str, str] | None:
    """ Returns tuple(jwt_token, refresh_token) or None on fail"""
    
    user_data = u_repo.get_user_by_username(username)
    if user_data is None:
        return None
    
    
    #TODO: _verify_password[ password, ress.password]
    if not _verify_password(password, asd):
        return None
    
    jwt_payload = _generate_jwt_payload() #TODO pass payload_data 
    jwt_token = _create_access_token(jwt_payload) 
    # returned 
    refresh_token = _create_refresh_token()
    
    # saved to db
    hashed_refresh_token = _hash_refresh_token(refresh_token)
    #TODO: user_repo: update_refresh_token [user_id, token_hash,expires_at]
    
    return (jwt_token, refresh_token)

def refresh(refresh_token: str):
    """Validate a refresh token and return a new access JWT."""
    
    hashed_refresh_token = _hash_refresh_token(refresh_token)
    
    
    expires_at = expires_at.replace(tzinfo=timezone.utc)
    

def logout(refresh_token: str):
    
    hashed_refresh_token = _hash_refresh_token(refresh_token)
    
    
    # 2. Find the refresh-token record by hash. extract[user_id, username, role, expires_at, revoked]
    #    If not found, return None.
    # 3. Check expiration and revocation.
    #    If invalid, return None.
    # 4. Retrieve the associated user.
    #    If not found, return None.
    # 5. Generate a new JWT using the user's claims.
    # 6. Return the new access JWT.
    
    #TODO: set revoked=True in refresh_tokens table for the matching hashed_refresh_token
    
    

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






