from abc import ABC, abstractmethod
from datetime import timedelta

from db.cache.redis.redis import get_redis


class AbstractCacheTokenRepository(ABC):
    @abstractmethod
    async def is_exists(self, token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_token(self, token: str, living_time: timedelta) -> None:
        raise NotImplementedError
