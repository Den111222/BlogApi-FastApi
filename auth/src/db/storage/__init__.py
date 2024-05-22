from abc import ABC, abstractmethod
from uuid import UUID

from models.schemas.user import CreateUser, User
from db.storage.postgre.postgre_session import get_session


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_user(self, _user_id: UUID) -> User | None:
        raise NotImplementedError

    async def get_user_by_login(self, login: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user: CreateUser, is_superuser: bool) -> User:
        raise NotImplementedError

    @abstractmethod
    async def check_if_exists(self, login: str, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_password_hash(self, login: str) -> str | None:
        raise NotImplementedError
