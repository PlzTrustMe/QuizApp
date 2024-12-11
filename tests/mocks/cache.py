from app.core.interfaces.cache import CacheGateway


class FakeCache(CacheGateway):
    def __init__(self):
        self.cache = {}
        self.member_keys = {}

        self.cached = False

    async def set_cache(self, key: str, value: dict, ttl: int) -> None:
        self.cache[key] = value

        self.cached = True

    async def get_cache(self, key: str) -> dict | None:
        return self.cache[key] if self.cache[key] else None

    async def set_member_key(self, member_key: str, cached_key: str) -> None:
        self.member_keys[member_key] = cached_key

    async def get_member_data(self, member_key: str) -> set | None:
        return (
            set(self.member_keys[member_key])
            if self.member_keys[member_key]
            else None
        )
