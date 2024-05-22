from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from models.schemas.tag import TagDelete, TagBase
from models.schemas.models_base import BaseResponseBody
from services.auth_service import security_jwt
from services.tag import TagService, get_tag_service

router = APIRouter(prefix="/tags", tags=["Tag"])


@router.get(
    "/",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Read all tags.",
    description="Read all tags.",
)
async def read_tags(
    token_data: Annotated[dict, Depends(security_jwt)],
    service: TagService = Depends(get_tag_service),
    page: int = 1,
    page_size: int = 5,
):
    result = await service.get_tags(page, page_size)
    return result


@router.post("/create_tag", response_model=BaseResponseBody)
async def create_tag(
    tag: TagBase,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: TagService = Depends(get_tag_service),
):
    result = await service.create_tag(token_data, tag)
    return result


@router.put(
    "/update_tag",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Update category.",
    description="Update category.",
)
async def update_tag(
    tag: TagBase,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: TagService = Depends(get_tag_service),
):
    result = await service.update_tag(token_data, tag)
    return result


@router.delete(
    "/full_delete_tag",
    response_model=BaseResponseBody,
    status_code=status.HTTP_200_OK,
    summary="Delete tag from database.",
    description="Delete tag from database.",
)
async def full_delete_tag(
    tag: TagDelete,
    token_data: Annotated[dict, Depends(security_jwt)],
    service: TagService = Depends(get_tag_service),
):
    result = await service.full_delete_tag(token_data, tag)
    return result
