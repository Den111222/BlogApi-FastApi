import uuid
from datetime import datetime

from db.storage import AbstractPostRepository
from fastapi import Depends, HTTPException

from db.storage.repo_factory import get_post_repo
from models.schemas.models_base import BaseResponseBody
from models.schemas.post import (
    PostCreate,
    PostUpdate,
    PostUpdateCategory,
    PostAddTag,
    PostDelete,
)


class PostService:
    def __init__(self, repo: AbstractPostRepository):
        self._repo = repo

    async def get_posts_by_author(
        self, token_data: dict, page: int, page_size: int
    ) -> BaseResponseBody:
        posts = await self._repo.get_posts_by_author(
            token_data["login"], page, page_size
        )
        return BaseResponseBody(data={"posts": posts})

    async def get_post(
        self, token_data: dict, post_id: uuid = None, title: str = None
    ) -> BaseResponseBody:
        if title is not None:
            result = await self._repo.get_post_by_title_author(
                title, token_data["login"]
            )
            if result is None:
                raise HTTPException(status_code=404, detail=f"Not found post '{title}'")
            return BaseResponseBody(data={"post": result})
        elif post_id is not None:
            result = await self._repo.get_post_by_id(post_id)
            if result is None:
                raise HTTPException(
                    status_code=404, detail=f"Not found post '{post_id}'"
                )
            return BaseResponseBody(data={"post": result})
        else:
            raise HTTPException(
                status_code=404, detail="Post can not be found like that..."
            )

    async def create_post(
        self, token_data: dict, _post: PostCreate
    ) -> BaseResponseBody:
        _post.author_login = token_data["login"]
        exist_post = await self._repo.if_exist(_post.title, token_data["login"])
        if exist_post:
            raise HTTPException(
                status_code=409, detail=f"Post '{_post.title}' - already exist"
            )
        else:
            post = await self._repo.create_post(_post)
            return BaseResponseBody(data={"post": post})

    async def update_post(
        self,
        token_data: dict,
        _post: PostUpdate | PostUpdateCategory | PostAddTag | PostDelete,
    ) -> BaseResponseBody:
        update_data = _post.model_dump()
        post = await self._repo.update_post(token_data["login"], _post.id, update_data)
        if post is None:
            raise HTTPException(
                status_code=422, detail=f"Post {_post.id} - not updated"
            )
        return BaseResponseBody(data={"post": post})

    async def public_post(self, token_data: dict, post_id: uuid) -> BaseResponseBody:
        update_data = {"published": True, "published_ad": datetime.utcnow()}
        post = await self._repo.update_post(token_data["login"], post_id, update_data)
        if post is None:
            raise HTTPException(
                status_code=422, detail=f"Post {post_id} - not publicated"
            )
        return BaseResponseBody(data={"post": post})

    async def full_delete_post(
        self, token_data: dict, _post: PostDelete
    ) -> BaseResponseBody:
        post = await self._repo.delete_post(token_data["login"], _post.id)
        if post is None:
            raise HTTPException(status_code=404, detail=f"Not found post '{_post.id}'")
        return BaseResponseBody(data={"Deleted post": post})


def get_post_service(
    repo: AbstractPostRepository = Depends(get_post_repo),
) -> PostService:
    return PostService(repo)
