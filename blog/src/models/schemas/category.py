from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    id: UUID
    name: str
    text: str | None
    deleted: bool

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str
    text: str | None


class CategoryUpdate(BaseModel):
    id: UUID
    name: str
    text: str | None


class CategoryDelete(BaseModel):
    id: UUID
    deleted: bool = True


class CategoryList(BaseModel):
    count_categories: int
    categories: list[Category]
