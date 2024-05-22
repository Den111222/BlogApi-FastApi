from uuid import UUID

from pydantic import BaseModel


class TagBase(BaseModel):
    name: str


class TagDelete(BaseModel):
    id: UUID


class Tag(TagBase, TagDelete):
    class Config:
        from_attributes = True


class TagList(BaseModel):
    count_tags: int
    tags: list[Tag]
