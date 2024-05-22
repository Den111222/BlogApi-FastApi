from uuid import uuid4

from sqlalchemy import select, update, func, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import selectinload

from db.storage import AbstractPostRepository
from models.schemas.post import PostList, Post, PostCreate, PostCreated
from models.db.post import Post as DBTablePost
from models.db.tag import Tag as DBTableTag


class PostRepository(AbstractPostRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def if_exist(self, title: str, author_login: str) -> Post | None:
        stmt = select(DBTablePost).filter_by(
            author_login=author_login, title=title, deleted=False
        )

        result = await self._db.execute(stmt)
        result = result.one_or_none()

        if result is None:
            return False

        return True

    async def get_post_by_id(self, id: UUID) -> Post | None:
        stmt = (
            select(DBTablePost)
            .filter(DBTablePost.id == id)
            .options(selectinload(DBTablePost.tags))
        )

        result = await self._db.execute(stmt)
        result = result.scalar_one_or_none()

        if result is not None:
            return Post.model_validate(result)

    async def get_post_by_title_author(self, title, author_login) -> Post | None:
        stmt = (
            select(DBTablePost)
            .filter_by(author_login=author_login, title=title, deleted=False)
            .options(selectinload(DBTablePost.tags))
        )

        result = await self._db.execute(stmt)
        result = result.scalar_one_or_none()

        if result is not None:
            return Post.model_validate(result)

    async def get_posts_by_author(
        self, author_login: str, page: int, page_size: int
    ) -> PostList | None:
        offset = (page - 1) * page_size

        # Count of all posts
        count_stmt = select(func.count(DBTablePost.id)).filter(
            DBTablePost.author_login == author_login, DBTablePost.deleted == False
        )
        total_posts_result = await self._db.execute(count_stmt)
        total_posts = total_posts_result.scalar_one()

        # Get posts with pagination
        # Many-to-many works only that (https://matt.sh/sqlalchemy-the-async-ening)
        stmt = (
            select(DBTablePost)
            .filter(
                DBTablePost.author_login == author_login, DBTablePost.deleted == False
            )
            .options(selectinload(DBTablePost.tags))
            .offset(offset)
            .limit(page_size)
        )

        result = await self._db.execute(stmt)
        result = result.all()

        if result is not None:
            posts = [Post.model_validate(*post) for post in result]
            return PostList(
                account_login=author_login, count_posts=total_posts, posts=posts
            )

    async def create_post(self, _post: PostCreate) -> PostCreated:
        db_file = DBTablePost(id=uuid4(), **_post.model_dump())

        self._db.add(db_file)
        try:
            await self._db.commit()
        except IntegrityError:
            await self._db.rollback()
            return None

        await self._db.refresh(db_file)

        return PostCreated.model_validate(db_file)

    async def update_post(
        self, author_login: str, post_id: UUID, update_data: dict
    ) -> Post:
        upd_values = {
            key: value for key, value in update_data.items() if value is not None
        }

        stmt = (
            select(DBTablePost)
            .where(DBTablePost.id == post_id, DBTablePost.deleted == False)
            .options(selectinload(DBTablePost.tags))
        )
        result = await self._db.execute(stmt)
        post = result.scalar_one_or_none()

        if post is None or post.author_login != author_login:
            return None

        db_tags = []
        if "tags" in upd_values:
            for tag_schema in upd_values["tags"]:
                stmt = (
                    select(DBTableTag)
                    .filter_by(name=tag_schema["name"])
                    .options(selectinload(DBTableTag.posts))
                )
                result = await self._db.execute(stmt)
                tag = result.scalar_one_or_none()

                if tag is None:
                    return None
                db_tags.append(tag)

        if db_tags != []:
            post.tags = db_tags
            try:
                await self._db.commit()
            except IntegrityError:
                await self._db.rollback()
                return None
            return Post.model_validate(post)
        else:
            stmt = (
                update(DBTablePost)
                .where(DBTablePost.id == post_id)
                .values(upd_values)
                .returning(DBTablePost)
            ).options(selectinload(DBTablePost.tags))

            try:
                result = await self._db.execute(stmt)
                await self._db.commit()
            except IntegrityError:
                await self._db.rollback()
                return None

        updated_post = result.scalar_one_or_none()

        if updated_post is not None:
            return Post.model_validate(updated_post)
        return None

    async def delete_post(self, author_login: str, post_id: UUID) -> Post:
        stmt = (
            delete(DBTablePost)
            .where(DBTablePost.id == post_id, DBTablePost.author_login == author_login)
            .returning(DBTablePost)
        ).options(selectinload(DBTablePost.tags))

        try:
            results = await self._db.execute(stmt)
        except IntegrityError:
            return None

        await self._db.commit()

        post = results.scalar_one_or_none()
        if post:
            return Post.model_validate(post)
