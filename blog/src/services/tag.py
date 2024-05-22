from fastapi import Depends, HTTPException

from db.storage import AbstractTagRepository
from db.storage.repo_factory import get_tag_repo
from models.schemas.tag import TagBase, TagDelete
from models.schemas.models_base import BaseResponseBody


class TagService:
    def __init__(self, repo: AbstractTagRepository):
        self._repo = repo

    async def get_tags(self, page: int, page_size: int) -> BaseResponseBody:
        tags = await self._repo.get_tags(page, page_size)
        return BaseResponseBody(data={"tags": tags})

    async def create_tag(self, token_data: dict, _tag: TagBase) -> BaseResponseBody:
        if token_data["is_superuser"]:
            exist_tag = await self._repo.if_exist(_tag.name)
            if exist_tag:
                raise HTTPException(
                    status_code=409, detail=f"Tag '{_tag.name}' - already exist"
                )
            else:
                tag = await self._repo.create_tag(_tag)
                return BaseResponseBody(data={"tag": tag})
        else:
            raise HTTPException(
                status_code=401, detail="Do not have permission to get tags"
            )

    async def update_tag(self, token_data: dict, _tag: TagBase) -> BaseResponseBody:
        if token_data["is_superuser"]:
            update_data = _tag.model_dump()
            tag = await self._repo.update_tag(_tag.id, update_data)
            if tag is None:
                raise HTTPException(
                    status_code=422, detail=f"Tag {_tag.id} - not updated"
                )
            return BaseResponseBody(data={"tag": tag})
        else:
            raise HTTPException(
                status_code=401, detail="Do not have permission to get tags"
            )

    async def full_delete_tag(
        self, token_data: dict, _tag: TagDelete
    ) -> BaseResponseBody:
        if token_data["is_superuser"]:
            tag = await self._repo.delete_tag(_tag.id)
            if tag is None:
                raise HTTPException(
                    status_code=404, detail=f"Not found post '{_tag.id}'"
                )
            return BaseResponseBody(data={"Deleted tag": tag})
        else:
            raise HTTPException(
                status_code=401, detail="Do not have permission to get tags"
            )


def get_tag_service(repo: AbstractTagRepository = Depends(get_tag_repo)) -> TagService:
    return TagService(repo)
