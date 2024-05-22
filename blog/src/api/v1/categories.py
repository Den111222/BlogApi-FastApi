from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from models.schemas.category import CategoryCreate, CategoryDelete, CategoryUpdate
from models.schemas.models_base import BaseResponseBody
from services.auth_service import security_jwt
from services.category import CategoryService, get_category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get(
    "/",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Read all categories.",
    description="Read all categories.",
)
async def read_categories(
    token_data: Annotated[dict, Depends(security_jwt)],
    service: CategoryService = Depends(get_category_service),
    page: int = 1,
    page_size: int = 5,
):
    result = await service.get_categories(token_data, page, page_size)
    return result


@router.get(
    "/detail",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Read category.",
    description="Read category.",
)
async def read_category(
    token_data: Annotated[dict, Depends(security_jwt)],
    service: CategoryService = Depends(get_category_service),
    category_id: UUID = None,
    name: str = None,
):
    result = await service.get_category(token_data, category_id, name)
    return result


@router.post(
    "/create_category",
    response_model=BaseResponseBody,
    status_code=status.HTTP_201_CREATED,
    summary="Create category.",
    description="Create category.",
)
async def create_category(
    category: CategoryCreate,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: CategoryService = Depends(get_category_service),
):
    result = await service.create_category(token_data, category)
    return result


@router.put(
    "/update_category",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Update category.",
    description="Update category.",
)
async def update_category(
    category: CategoryUpdate,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: CategoryService = Depends(get_category_service),
):
    result = await service.update_category(token_data, category)
    return result


@router.put(
    "/delete_category",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Make mark 'Deleted' by category.",
    description="Make mark 'Deleted' by category.",
)
async def delete_category(
    category: CategoryDelete,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: CategoryService = Depends(get_category_service),
):
    result = await service.update_category(token_data, category)
    return result


@router.delete(
    "/full_delete_category",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Delete category from database.",
    description="Delete category from database.",
)
async def full_delete_category(
    post: CategoryDelete,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: CategoryService = Depends(get_category_service),
):
    result = await service.full_delete_category(token_data, post)
    return result
