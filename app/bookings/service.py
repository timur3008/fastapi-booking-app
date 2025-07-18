from datetime import date

import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from app.logger import logger
from app.bookings.models import Booking
from app.database import async_session_maker, engine
from app.hotels.models import Room
from app.services.base import BaseService


class BookingService(BaseService):
    model = Booking

    @classmethod
    async def add_booking(
        cls, user_id: int, room_id: int, date_from: date, date_to: date
    ):
        """
        WITH booked_rooms AS (SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2023-05-15' AND date_from <= '2023-06-25') OR
            (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )

        SELECT rooms.quantity - COUNT(booked_rooms.id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id;
        """
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    sa.select(Booking)
                    .where(
                        sa.and_(
                            Booking.room_id == 1,
                            sa.or_(
                                sa.and_(
                                    Booking.date_from >= date_from,
                                    Booking.date_from <= date_to,
                                ),
                                sa.and_(
                                    Booking.date_from <= date_from,
                                    Booking.date_to > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )
                rooms_left_query = (
                    sa.select(
                        (Room.quantity - sa.func.count(booked_rooms.c.room_id)).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Room)
                    .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
                    .where(Room.id == room_id)
                    .group_by(Room.quantity, booked_rooms.c.room_id)
                )
                rooms_left = await session.execute(rooms_left_query)
                # print(rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))
                rooms_left = rooms_left.scalar()
                if not rooms_left or rooms_left > 0:
                    get_price_query = sa.select(Room.price).filter_by(id=room_id)
                    price = await session.execute(get_price_query)
                    price: int = price.scalar()
                    add_booking_query = (
                        sa.insert(Booking)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Booking)
                    )
                    new_booking = await session.execute(add_booking_query)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    return None
        except (SQLAlchemyError, Exception) as exc:
            if isinstance(exc, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(exc, Exception):
                msg = "Unknown Exc"
            msg += ": Connot add booking"
            extra = {"user_id": user_id, "room_id": room_id, "date_from": date_from, "date_to": date_to}
            logger.error(msg=msg, extra=extra, exc_info=True)