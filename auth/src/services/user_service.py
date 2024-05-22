from fastapi import Depends
from passlib.hash import pbkdf2_sha256

from db.storage import AbstractUserRepository
from db.storage.repo_factory import get_user_repo
from models.schemas.user import CreateUser, User


class UserService:
    def __init__(self, repo: AbstractUserRepository):
        self._repo = repo

    async def create_user(self, user: CreateUser, is_superuser: bool = False) -> User:
        pwd = pbkdf2_sha256.hash(user.password)
        user.password = pwd
        return await self._repo.create_user(user, is_superuser)

    async def get_user_by_login(self, login: str) -> User | None:
        return await self._repo.get_user_by_login(login)

    async def check_password(self, login: str, password: str) -> bool:
        password_hash = await self._repo.get_password_hash(login)

        if password_hash is None:
            return False

        return pbkdf2_sha256.verify(password, password_hash)

    async def check_credentials(self, login: str, password: str) -> User | None:
        is_checked = await self.check_password(login, password)

        if is_checked:
            return await self.get_user_by_login(login)

    async def check_is_exists(self, login: str, email: str) -> bool:
        return await self._repo.check_if_exists(login, email)


def get_user_service(
    repo: AbstractUserRepository = Depends(get_user_repo),
) -> UserService:
    return UserService(repo)
