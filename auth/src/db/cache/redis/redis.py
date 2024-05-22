from redis.asyncio import Redis

from core.config import app_settings


async def get_redis() -> Redis:
    redis = Redis(host=app_settings.redis_host, port=app_settings.redis_port)
    yield redis
    await redis.close()
