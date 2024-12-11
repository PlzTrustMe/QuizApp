import json

from redis.asyncio import Redis

from app.core.interfaces.cache import CacheGateway


class RedisCache(CacheGateway):
    def __init__(self, redis: Redis):
        self.redis = redis

    def _convert_value_to_json(self, value: dict) -> str:
        return json.dumps(value)

    def _convert_json_to_dict(self, json_data: str) -> dict:
        return json.loads(json_data)

    async def set_cache(self, key: str, value: dict, ttl: int) -> None:
        converted_value = self._convert_value_to_json(value)

        await self.redis.setex(key, ttl, converted_value)

    async def get_cache(self, key: str) -> dict | None:
        data = await self.redis.get(key)

        return None if not data else self._convert_json_to_dict(data)

    async def set_member_key(self, member_key: str, cached_key: str) -> None:
        await self.redis.sadd(member_key, cached_key)

    async def get_member_data(self, member_key: str) -> set | None:
        return await self.redis.smembers(member_key)
