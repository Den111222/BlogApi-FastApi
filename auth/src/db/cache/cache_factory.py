from functools import lru_cache

from fastapi import Depends
from redis import Redis

from db.cache import get_redis
from db.cache.redis.token import RedisTokenRepository


@lru_cache()
def get_token_cache(
    session: Redis = Depends(get_redis),
) -> RedisTokenRepository:
    return RedisTokenRepository(session)
