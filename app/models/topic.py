from datetime import datetime
from pydantic import BaseModel, StrictBool, ConfigDict, Field, model_validator
from typing import Annotated, Generic, TypeVar
from enum import Enum

TopicTitle = Annotated[str, Field(min_length= 2, max_length= 128)]
TopicContent = Annotated[str, Field(min_length= 2, max_length= 8192)]
PositiveId = Annotated[int, Field(gt=0)]
Username = Annotated[str, Field(min_length= 2, max_length= 16, pattern=r"^[A-Za-z0-9_]+$")]


class UserSummary(BaseModel):
    user_id: PositiveId
    username: str


class CategorySummary(BaseModel):
    category_id: PositiveId
    category_name: str


class StrictInput(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)


class TopicLockRequest(StrictInput):
    is_locked: StrictBool


class TopicVisibility(StrictInput):
    is_private: StrictBool


class BestReplyRequest(StrictInput):
    reply_id: PositiveId


class TopicInviteRequest(StrictInput):
    username: Username


class TopicSortBy(str, Enum):
    CREATED_AT = 'created_at'
    REPLY_COUNT = 'reply_count'


class SortOrder(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class TopicListQuery(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)

    search: str | None = Field(default=None, max_length= 128)
    category_id: PositiveId | None = None
    sort_by: TopicSortBy = TopicSortBy.CREATED_AT
    sort_order: SortOrder = SortOrder.DESC
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class TopicCreate(BaseModel):
    title: TopicTitle
    content: TopicContent
    is_private: StrictBool = False
    category_id: PositiveId


class TopicUpdate(BaseModel):
    title: TopicTitle | None = None
    content: TopicContent | None = None
    category_id: PositiveId | None = None

    @model_validator(mode='after')
    def at_least_one_field(self):
        if self.title is None and self.content is None and self.category_id is None:
            raise ValueError('At least one field is required to Update')

        return self


class StoredTopic(BaseModel):
    topic_id: PositiveId
    title: TopicTitle
    content: TopicContent
    is_locked: bool
    is_private: bool
    author_id: PositiveId
    category_id: PositiveId
    best_reply_id: PositiveId | None = None
    created_at: datetime


class TopicListItem(BaseModel):
    topic_id: PositiveId
    title: str
    author: UserSummary
    category: CategorySummary
    is_locked: bool
    is_private: bool
    reply_count: int = Field(ge=0)
    created_at: datetime


class TopicDetail(BaseModel):
    content: str
    best_reply_id: PositiveId | None = None


T = TypeVar('T')


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    limit: int = Field(ge=1)


class InvitationStatus(str, Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'

    @classmethod
    def from_db(cls, is_accepted: int | None, answered_at: datetime | None) -> 'InvitationStatus':
        if is_accepted == 1:
            return cls.ACCEPTED
        if answered_at is not None:
            return cls.DECLINED
        return cls.PENDING


class InvitationResponse(BaseModel):
    topic_id: PositiveId
    user: UserSummary
    status: InvitationStatus
    answered_at: datetime | None = None
