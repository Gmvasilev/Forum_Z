"""Password hashing and JWT token utilities."""

from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
import base64
import hashlib

from app.config import settings




def _prepare_password(password: str) -> bytes:
    """Convert a string password into a 44-byte Base64 SHA-256 digest safe for bcrypt."""
    
    raw_bytes = password.encode("utf-8") # raw UTF-8 bytes
    digest = hashlib.sha256(raw_bytes).digest() # 32 bytes long
    return base64.b64encode(digest) # convert into a 44-byte Base64 ASCII byte string 


def hash_password(password: str) -> str:
    """Hash a string password using SHA-256 pre-hashing and bcrypt."""
    
    prepared = _prepare_password(password)
    salt = bcrypt.gensalt() # salt is contained in the hash
    hashed = bcrypt.hashpw(prepared, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    
    prepared = _prepare_password(plain_password)
    return bcrypt.checkpw(
        prepared, hashed_password.encode("utf-8")
    )


# --- JWT tokek payload : 
#- "sub"     : user_id 
#- "username": username
#- "role"    : user_role
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token with the given payload data."""
    
    to_encode = data.copy()
    
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





