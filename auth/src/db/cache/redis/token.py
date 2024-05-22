from datetime import timedelta
from redis.asyncio import Redis

from db.cache import AbstractCacheTokenRepository


class RedisTokenRepository(AbstractCacheTokenRepository):
    def __init__(self, redis: Redis):
        self._db = redis

    async def save_token(self, token: str, living_time: timedelta) -> None:
        await self._db.set(token, token, living_time)

    async def is_exists(self, token: str) -> bool:
        result = await self._db.get(token)
        return bool(result)
