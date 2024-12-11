from abc import abstractmethod
from asyncio import Protocol


class UploadFile(Protocol):
    @abstractmethod
    def upload_quiz(self, file: bytes) -> list[dict]:
        raise NotImplementedError
