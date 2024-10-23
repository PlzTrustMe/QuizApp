from sqlalchemy import exists, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.commands.errors import UnexpectedError
from app.core.entities.user import User
from app.core.interfaces.user_gateways import UserGateway
from app.infrastructure.persistence.models.user import users_table


class UserMapper(UserGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_exist(self, email: str) -> bool:
        query = select(exists().where(users_table.c.user_email == email))

        result = await self.session.execute(query)

        return result.scalar()

    async def add(self, user: User) -> None:
        self.session.add(user)

        try:
            await self.session.flush()
        except IntegrityError as error:
            raise UnexpectedError from error
