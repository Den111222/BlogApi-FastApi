import uuid

from fastapi import Depends, HTTPException

from db.storage import AbstractCategoryRepository
from db.storage.repo_factory import get_category_repo
from models.schemas.category import (
    Category,
    CategoryCreate,
    CategoryDelete,
    CategoryUpdate,
)
from models.schemas.models_base import BaseResponseBody


class CategoryService:
    def __init__(self, repo: AbstractCategoryRepository):
        self._repo = repo

    async def get_categories(
        self, token_data: dict, page: int, page_size: int
    ) -> BaseResponseBody:
        if token_data["is_superuser"]:
            categories = await self._repo.get_categories(page, page_size)
            return BaseResponseBody(data={"categories": categories})
        else:
            raise HTTPException(
                status_code=401, detail="Do not have permission to get categories"
            )

    async def get_category(
        self, token_data: dict, category_id: uuid = None, name: str = None
    ) -> BaseResponseBody:
        if token_data["is_superuser"]:
            if name is not None:
                result = await self._repo.get_category_by_name(name)
                if result is None:
                    raise HTTPException(
                        status_code=404, detail=f"No found category '{name}'"
                    )
                return BaseResponseBody(data={"category": result})
            elif category_id is not None:
                result = await self._repo.get_category_by_id(category_id)
                if result is None:
                    raise HTTPException(
                        status_code=404, detail=f"No found category '{category_id}'"
                    )
                return BaseResponseBody(data={"category": result})
            else:
                raise HTTPException(
                    status_code=404, detail="Category can not be found like that..."
                )
        else:
            raise HTTPException(
                status_code=401, detail="Do not have permission to get categories"
            )

    async def create_category(
        self, token_data: dict, _category: CategoryCreate
    ) -> BaseResponseBody:
        if token_data["is_superuser"]:
            exist_category = await self._repo.if_exist(_category.name)
            if exist_category:
                raise HTTPException(
                    status_code=409,
                    detail=f"Category '{_category.name}' - already exist",
                )
            else:
                category = await self._repo.create_category(_category)
                return BaseResponseBody(data={"category": category})
        else:
            raise HTTPException(
                status_code=401, detail="Do not have permission to get categories"
            )

    async def update_category(
        self, token_data: dict, _category: CategoryUpdate | CategoryDelete
    ) -> BaseResponseBody:
        if token_data["is_superuser"]:
            update_data = _category.model_dump()
            category = await self._repo.update_category(_category.id, update_data)
            if category is None:
                raise HTTPException(
                    status_code=422, detail=f"Category {_category.id} - not updated"
                )
            return BaseResponseBody(data={"category": category})
        else:
            raise HTTPException(
                status_code=401, detail="Do not have permission to get categories"
            )

    async def full_delete_category(
        self, token_data: dict, _category: CategoryDelete
    ) -> BaseResponseBody:
        if token_data["is_superuser"]:
            category = await self._repo.delete_category(_category.id)
            if category is None:
                raise HTTPException(
                    status_code=404, detail=f"Not found post '{_category.id}'"
                )
            return BaseResponseBody(data={"Deleted category": category})
        else:
            raise HTTPException(
                status_code=401, detail="Do not have permission to get categories"
            )


def get_category_service(
    repo: AbstractCategoryRepository = Depends(get_category_repo),
) -> CategoryService:
    return CategoryService(repo)
