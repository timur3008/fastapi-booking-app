import sqlalchemy as sa

from app.database import async_session_maker
from app.hotels.models import Hotel, Room
from app.services.base import BaseService

from .models import Hotel, Room


class HotelService(BaseService):
    model = Hotel

    @classmethod
    async def get_hotels_by_location(cls, location: str):
        async with async_session_maker() as session:
            query = sa.select(Hotel).where(Hotel.location.ilike(f"%{location}%"))
            result = await session.execute(query)
            return result.scalars().all()


class RoomService(BaseService):
    model = Room