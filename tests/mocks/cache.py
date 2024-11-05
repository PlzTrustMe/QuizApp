from app.core.interfaces.cache import CacheGateway


class FakeCache(CacheGateway):
    def __init__(self):
        self.cache = {}

        self.cached = False

    async def set_cache(self, key: str, value: dict, ttl: int) -> None:
        self.cache[key] = value

        self.cached = True
