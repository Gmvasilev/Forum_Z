from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class ReactionType(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"

    @classmethod
    def from_db(cls, value: int) -> ReactionType:
        if value == 1:
            return ReactionType.LIKE
        elif value == 0:
            return ReactionType.DISLIKE
        else:
            raise ValueError(f"Unexpected reaction in database {value}")

    def to_db(self) -> int:
        return 1 if self == ReactionType.LIKE else 0

class ReactionRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')

    reaction_type: ReactionType

class StoredReaction(BaseModel):
    user_id: int = Field(gt=0)
    reply_id: int = Field(gt=0)
    reaction_type: ReactionType

class ReactionResponse(BaseModel):
    reply_id: int = Field(gt=0)
    like_count: int = Field(gt=0)
    dislike_count: int = Field(gt=0)
    current_user_reaction: ReactionRequest | None = None

