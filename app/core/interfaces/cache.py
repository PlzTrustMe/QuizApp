from abc import abstractmethod
from asyncio import Protocol


class CacheGateway(Protocol):
    @abstractmethod
    async def set_cache(self, key: str, value: dict, ttl: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_cache(self, key: str) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    async def set_member_key(self, member_key: str, cached_key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_member_data(self, member_key: str) -> set | None:
        raise NotImplementedError
