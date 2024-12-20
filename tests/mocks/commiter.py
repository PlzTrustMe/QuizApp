from app.core.common.commiter import Commiter


class FakeCommiter(Commiter):
    def __init__(self):
        self.commited = False

    async def commit(self) -> None:
        self.commited = True
