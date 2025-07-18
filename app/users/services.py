import sqlalchemy as sa

from app.database import async_session_maker
from app.services.base import BaseService
from app.users.models import User


class UserService(BaseService):
    model = User

    @classmethod
    async def add_data(cls, email: str, hashed_password: str):
        async with async_session_maker() as session:
            query = sa.insert(User).values(email=email, hashed_password=hashed_password).returning(User)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()