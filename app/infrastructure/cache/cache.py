import json

from redis.asyncio import Redis

from app.core.interfaces.cache import CacheGateway


class RedisCache(CacheGateway):
    def __init__(self, redis: Redis):
        self.redis = redis

    def _convert_value_to_json(self, value: dict) -> str:
        return json.dumps(value)

    async def set_cache(self, key: str, value: dict, ttl: int) -> None:
        converted_value = self._convert_value_to_json(value)

        await self.redis.setex(key, ttl, converted_value)
