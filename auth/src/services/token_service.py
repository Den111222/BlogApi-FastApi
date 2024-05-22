from datetime import datetime

import jwt
from jwt import ExpiredSignatureError
from fastapi import Depends

from core.config import app_settings
from db.cache import AbstractCacheTokenRepository
from db.cache.cache_factory import get_token_cache

from models.schemas.token import Tokens
from models.schemas.user import UserPayload


class TokenService:
    def __init__(self, cache: AbstractCacheTokenRepository):
        self._cache = cache

    @staticmethod
    async def create_token(login: str, payload: dict = None) -> Tokens:
        if not payload:
            payload = {}

        access_token = jwt.encode(
            {
                "login": login,
                "exp": datetime.now() + app_settings.access_live,
                **payload,
            },
            app_settings.token_secret,
            algorithm=app_settings.algorithm,
        )

        refresh_token = jwt.encode(
            {
                "login": login,
                "exp": datetime.now() + app_settings.refresh_live,
                **payload,
            },
            app_settings.token_secret,
            algorithm=app_settings.algorithm,
        )

        return Tokens(access_token=access_token, refresh_token=refresh_token)

    async def check_token(self, token: str) -> UserPayload | None:
        is_exists = await self._cache.is_exists(token)

        if is_exists:
            return None

        try:
            payload = jwt.decode(
                token, app_settings.token_secret, algorithms=[app_settings.algorithm]
            )
        except ExpiredSignatureError:
            return None

        return UserPayload.model_validate(payload)

    async def deactivate_tokens(
        self, refresh: str | None = None, access: str | None = None
    ):
        if refresh is not None:
            await self._cache.save_token(refresh, app_settings.refresh_live)

        if access is not None:
            await self._cache.save_token(access, app_settings.access_live)


def get_token_service(
    cache_repo: AbstractCacheTokenRepository = Depends(get_token_cache),
) -> TokenService:
    return TokenService(cache_repo)
