from uuid import UUID, uuid4

from sqlalchemy import select, func, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.storage import AbstractCategoryRepository
from models.db.category import Category as DBTableCategory
from models.schemas.category import CategoryList, Category, CategoryCreate


class CategoryRepository(AbstractCategoryRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_category_by_id(self, id: UUID) -> Category | None:
        stmt = select(DBTableCategory).filter(DBTableCategory.id == id)

        result = await self._db.execute(stmt)
        result = result.scalar_one_or_none()

        if result is not None:
            return Category.model_validate(result)

    async def get_category_by_name(self, name: str) -> Category | None:
        stmt = select(DBTableCategory).filter(DBTableCategory.name == name)

        result = await self._db.execute(stmt)
        result = result.scalar_one_or_none()

        if result is not None:
            return Category.model_validate(result)

    async def get_categories(self, page: int, page_size: int) -> CategoryList | None:
        offset = (page - 1) * page_size

        count_stmt = select(func.count(DBTableCategory.id))
        total_result = await self._db.execute(count_stmt)
        total = total_result.scalar_one()

        stmt = select(DBTableCategory).offset(offset).limit(page_size)

        result = await self._db.execute(stmt)
        result = result.all()

        if result is not None:
            categories = [Category.model_validate(*category) for category in result]
            return CategoryList(count_categories=total, categories=categories)

    async def create_category(self, _category: CategoryCreate) -> Category:
        db_file = DBTableCategory(id=uuid4(), **_category.model_dump())

        self._db.add(db_file)
        try:
            await self._db.commit()
        except IntegrityError:
            await self._db.rollback()
            return None

        await self._db.refresh(db_file)

        return Category.model_validate(db_file)

    async def update_category(self, category_id: UUID, update_data: dict) -> Category:
        upd_values = {
            key: value for key, value in update_data.items() if value is not None
        }

        stmt = (
            update(DBTableCategory)
            .where(DBTableCategory.id == category_id)
            .values(upd_values)
            .returning(DBTableCategory)
        )

        try:
            result = await self._db.execute(stmt)
            await self._db.commit()
        except IntegrityError:
            await self._db.rollback()
            return None

        updated_category = result.scalar_one_or_none()

        if updated_category is not None:
            return Category.model_validate(updated_category)
        return None

    async def delete_category(self, category_id: UUID) -> Category:
        stmt = (
            delete(DBTableCategory)
            .where(DBTableCategory.id == category_id)
            .returning(DBTableCategory)
        )

        try:
            results = await self._db.execute(stmt)
        except IntegrityError:
            return None

        await self._db.commit()

        post = results.scalar_one_or_none()
        if post:
            return Category.model_validate(post)

    async def if_exist(self, name: str) -> bool:
        stmt = select(DBTableCategory).filter_by(name=name)

        result = await self._db.execute(stmt)
        result = result.one_or_none()

        if result is None:
            return False

        return True
