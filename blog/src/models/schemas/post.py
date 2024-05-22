from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from models.schemas.tag import Tag


class PostBase(BaseModel):
    title: str
    created_ad: datetime
    published_ad: datetime | None
    published: bool = False
    deleted: bool = False
    category_id: UUID
    tags: list[Tag]


class PostCreate(BaseModel):
    author_login: str = Field(default="", exclude=False)
    title: str
    text: str
    category_id: UUID

    model_config = ConfigDict(from_attributes=True, extra="forbid")


class PostCreated(BaseModel):
    id: UUID
    title: str
    text: str
    published: bool = False
    category_id: UUID

    model_config = ConfigDict(from_attributes=True)


class Post(PostBase):
    id: UUID

    class Config:
        from_attributes = True


class PostList(BaseModel):
    account_login: str
    count_posts: int
    posts: list[Post]


class PostUpdate(BaseModel):
    id: UUID
    title: str | None
    text: str | None


class PostUpdateCategory(BaseModel):
    id: UUID
    category_id: UUID | None


class PostAddTag(BaseModel):
    id: UUID
    tags: list[Tag] | None


class PostDelete(BaseModel):
    id: UUID
    deleted: bool = True
