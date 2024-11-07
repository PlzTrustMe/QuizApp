from abc import abstractmethod
from asyncio import Protocol


class CacheGateway(Protocol):
    @abstractmethod
    async def set_cache(self, key: str, value: dict, ttl: int) -> None:
        raise NotImplementedError
