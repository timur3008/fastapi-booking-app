import sqlalchemy as sa

from app.bookings.models import Booking
from app.database import async_session_maker


class BaseService:
    model = None

    @classmethod
    async def get_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = sa.select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = sa.select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all_items(cls, **filter_by):
        async with async_session_maker() as session:
            query = sa.select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()