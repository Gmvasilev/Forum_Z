# TODO: reply Pydantic models (field limits from the spec)
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ReplyResponse(BaseModel):
    reply_id : int
    topic_id : int
    author_id : int
    author_username : str
    content: str
    created_at : datetime
    likes : int
    dislikes : int

    @classmethod
    def from_query_result(cls,reply_id,topic_id,author_id,author_username,content,created_at,likes,dislikes):
        return cls(
            reply_id=reply_id,
            topic_id=topic_id,
            author_id=author_id,
            author_username=author_username,
            content=content,
            created_at=created_at,
            likes=likes,
            dislikes=dislikes
        )

class ReplyCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    content: str = Field(min_length=2, max_length=8192)

class ReplyUpdate(ReplyCreate):
    pass
