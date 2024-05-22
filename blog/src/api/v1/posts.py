from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from models.schemas.models_base import BaseResponseBody
from models.schemas.post import (
    PostCreate,
    PostUpdate,
    PostUpdateCategory,
    PostAddTag,
    PostDelete,
)
from services.auth_service import security_jwt
from services.post import PostService, get_post_service

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "/",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Read all posts by author.",
    description="Read all posts by author.",
)
async def read_posts(
    token_data: Annotated[dict, Depends(security_jwt)],
    service: PostService = Depends(get_post_service),
    page: int = 1,
    page_size: int = 5,
):
    result = await service.get_posts_by_author(token_data, page, page_size)
    return result


@router.get(
    "/detail",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Read post.",
    description="Read post.",
)
async def read_post(
    token_data: Annotated[dict, Depends(security_jwt)],
    service: PostService = Depends(get_post_service),
    post_id: UUID = None,
    title: str = None,
):
    result = await service.get_post(token_data, post_id, title)
    return result


@router.post(
    "/create_post",
    response_model=BaseResponseBody,
    status_code=status.HTTP_201_CREATED,
    summary="Create post.",
    description="Create post.",
)
async def create_post(
    post: PostCreate,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: PostService = Depends(get_post_service),
):
    result = await service.create_post(token_data, post)
    return result


@router.put(
    "/update_post",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Update post.",
    description="Update post.",
)
async def update_post(
    post: PostUpdate,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: PostService = Depends(get_post_service),
):
    result = await service.update_post(token_data, post)
    return result


@router.put(
    "/public_post",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Public post.",
    description="Public post.",
)
async def public_post(
    post_id: UUID,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: PostService = Depends(get_post_service),
):
    result = await service.public_post(token_data, post_id)
    return result


@router.put(
    "/chenge_category",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Change category for post.",
    description="Change category for post.",
)
async def chenge_category(
    post: PostUpdateCategory,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: PostService = Depends(get_post_service),
):
    result = await service.update_post(token_data, post)
    return result


@router.put(
    "/add_update_tags",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Add or update tags to post.",
    description="Add or update tags to post.",
)
async def add_update_tags(
    post: PostAddTag,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: PostService = Depends(get_post_service),
):
    result = await service.update_post(token_data, post)
    return result


@router.put(
    "/delete_post",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Make mark 'Deleted' by post.",
    description="Make mark 'Deleted' by post.",
)
async def delete_post(
    post: PostDelete,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: PostService = Depends(get_post_service),
):
    result = await service.update_post(token_data, post)
    return result


@router.delete(
    "/full_delete_post",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Delete post from database.",
    description="Delete post from database.",
)
async def full_delete_post(
    post: PostDelete,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: PostService = Depends(get_post_service),
):
    result = await service.full_delete_post(token_data, post)
    return result
