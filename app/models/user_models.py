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

PositiveId = Annotated[
    int,
    Field(gt=0)
]

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


#--- Stricter validation on creating password
PasswordCreate = Annotated[
    SecretStr,
    Field(min_length=8, max_length=254, examples=["StrongPassword123!"]),
    AfterValidator(_validate_password_strength)
]

#--- Used for comparison with the saved password
PasswordLogin = Annotated[
    SecretStr,
    Field(max_length=254)
]



# ------------------------------------------------------------------------
# -   Pydantic Models
# ------------------------------------------------------------------------


# --- Mixin class for multiple inheritance to achieve id as first attribute. ---


class UserIdMixin(BaseModel):
    user_id: PositiveId
    
class UserBase(BaseModel):
    first_name: FirstName
    last_name: LastName
    username: Username
    email: Email

class UserIn(UserBase):
    password: PasswordCreate
    #todo add password_confirm checked in the front end
    
class UserBaseOut(BaseModel):
    """ User public view """
    username: Username
    rating: float  # likes/disslikes ratio






class UserOut(UserIdMixin, UserBaseOut):
    pass


class UserWithPostsOut(UserOut):
    posts_ids: list[int] #TODO: list of Posts with id + title

class UserLogin(BaseModel):
    username: Username
    password: PasswordLogin
    
    
    