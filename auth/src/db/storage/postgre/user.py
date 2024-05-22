from uuid import uuid4, UUID

from sqlalchemy import or_, and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.storage import AbstractUserRepository
from models.schemas.user import CreateUser, User
from models.db.user import User as DBTableUser


class UserRepository(AbstractUserRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_user(self, _user_id: UUID) -> User | None:
        statement = select(DBTableUser).where(DBTableUser.id == _user_id)

        result = await self._db.execute(statement)
        result = result.scalar_one_or_none()

        if result is not None:
            return User.model_validate(result)

    async def get_user_by_login(self, login: str) -> User | None:
        statement = select(DBTableUser).where(DBTableUser.login == login)

        result = await self._db.execute(statement)
        result = result.scalar_one_or_none()

        if result is not None:
            return User.model_validate(result)

    async def create_user(self, _user: CreateUser, is_superuser: bool) -> User | None:
        db_user = DBTableUser(
            id=uuid4(), is_superuser=is_superuser, **_user.model_dump()
        )

        self._db.add(db_user)
        try:
            await self._db.commit()
        except IntegrityError:
            await self._db.rollback()
            return None

        await self._db.refresh(db_user)

        return User.model_validate(db_user)

    async def check_if_exists(self, login: str, email: str) -> bool:
        statement = select(DBTableUser).where(
            or_(DBTableUser.email == email, DBTableUser.login == login)
        )

        result = await self._db.execute(statement)
        result = result.one_or_none()

        if result is None:
            return False

        return True

    async def get_password_hash(self, login: str) -> str | None:
        statement = select(DBTableUser).where(and_(DBTableUser.login == login))

        result = await self._db.execute(statement)
        result = result.scalar_one_or_none()

        if result is not None:
            return result.password
