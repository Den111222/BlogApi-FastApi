from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.storage import get_session
from db.storage.postgre.category import CategoryRepository
from db.storage.postgre.post import PostRepository
from db.storage.postgre.tag import TagRepository


@lru_cache()
def get_post_repo(
    session: AsyncSession = Depends(get_session),
) -> PostRepository:
    return PostRepository(session)


@lru_cache()
def get_category_repo(
    session: AsyncSession = Depends(get_session),
) -> CategoryRepository:
    return CategoryRepository(session)


@lru_cache()
def get_tag_repo(
    session: AsyncSession = Depends(get_session),
) -> TagRepository:
    return TagRepository(session)
