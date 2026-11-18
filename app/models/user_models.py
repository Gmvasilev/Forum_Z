import re
from typing import Annotated
from pydantic import (
    BaseModel,
    Field,
    StringConstraints,
    EmailStr,
    SecretStr,
    AfterValidator
)




# ------------------------------------------------------------------------
# -   Internal field validator
# ------------------------------------------------------------------------


def _validate_password_strength(value: SecretStr) -> SecretStr:
    raw = value.get_secret_value()
    if not re.search(r"[A-Z]", raw):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", raw):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", raw):
        raise ValueError("Password must contain at least one number")
    return value



# ------------------------------------------------------------------------
# -   Reusable Field Types (Validation & OpenAPI Metadata)  
# ------------------------------------------------------------------------

FirstName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2, max_length=32),
    Field(examples=["Joshua"])
]

LastName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2, max_length=32),
    Field(examples=["Bolduin"])
]

Username = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2, max_length=16),
    Field(examples=["zoomer123"])
]

Email = Annotated[
    EmailStr,
    Field(min_length=6, max_length=254, examples=["zoomer123@abv.bg"])
]

Password = Annotated[
    SecretStr,
    Field(min_length=8, max_length=254, examples=["StrongPassword123!"]),
    AfterValidator(_validate_password_strength)
]



# ------------------------------------------------------------------------
# -   Pydantic Models
# ------------------------------------------------------------------------


# --- Mixin class for multiple inheritance to achieve id as first attribute. ---
class UserIdMixin(BaseModel):
    user_id: int


class UserBase(BaseModel):
    first_name: FirstName
    last_name: LastName
    username: Username
    email: Email


class UserIn(UserBase):
    password: Password
    
    
class UserOut(UserIdMixin, UserIn):
    pass


class UserLogin(BaseModel):
    username: Username
    password: Annotated[SecretStr, Field(max_length=254)]
    
    
    