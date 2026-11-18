# TODO: reply Pydantic models (field limits from the spec)
from pydantic import BaseModel, ConfigDict, Field

class ReplyCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    content: str = Field(min_length=2, max_length=8192)

class ReplyUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    content: str = Field(min_length=2, max_length=8192)
