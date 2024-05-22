from uuid import UUID, uuid4

from sqlalchemy import select, delete, update, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.storage import AbstractTagRepository
from models.db.tag import Tag as DBTableTag
from models.schemas.tag import Tag, TagList


class TagRepository(AbstractTagRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_tags(self, page: int, page_size: int) -> TagList | None:
        offset = (page - 1) * page_size

        count_stmt = select(func.count(DBTableTag.id))
        total_result = await self._db.execute(count_stmt)
        total = total_result.scalar_one()

        stmt = select(DBTableTag).offset(offset).limit(page_size)

        result = await self._db.execute(stmt)
        result = result.all()

        if result is not None:
            tags = [Tag.model_validate(*tag) for tag in result]
            return TagList(count_categories=total, categories=tags)

    async def create_tag(self, _tag: Tag) -> Tag:
        db_file = DBTableTag(id=uuid4(), **_tag.model_dump())

        self._db.add(db_file)
        try:
            await self._db.commit()
        except IntegrityError:
            await self._db.rollback()
            return None

        await self._db.refresh(db_file)

        return Tag.model_validate(db_file)

    async def update_tag(self, tag_id: UUID, update_data: dict) -> Tag:
        upd_values = {
            key: value for key, value in update_data.items() if value is not None
        }

        stmt = (
            update(DBTableTag)
            .where(DBTableTag.id == tag_id)
            .values(upd_values)
            .returning(DBTableTag)
        )

        try:
            result = await self._db.execute(stmt)
            await self._db.commit()
        except IntegrityError:
            await self._db.rollback()
            return None

        updated_tag = result.scalar_one_or_none()

        if updated_tag is not None:
            return Tag.model_validate(updated_tag)
        return None

    async def delete_tag(self, category_id: UUID) -> Tag:
        stmt = (
            delete(DBTableTag).where(DBTableTag.id == category_id).returning(DBTableTag)
        )

        try:
            results = await self._db.execute(stmt)
        except IntegrityError:
            return None

        await self._db.commit()

        post = results.scalar_one_or_none()
        if post:
            return Tag.model_validate(post)

    async def if_exist(self, name: str) -> bool:
        stmt = select(DBTableTag).filter_by(name=name)

        result = await self._db.execute(stmt)
        result = result.one_or_none()

        if result is None:
            return False

        return True
