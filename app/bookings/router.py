from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_versioning import version
from pydantic import parse_obj_as

from app import exceptions
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import User

from .schemas import BookingSchema
from .service import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)

@router.get("")
@version(1)
async def get_bookings(user: User = Depends(get_current_user)) -> list[BookingSchema]:
    return await BookingService.get_all_items(user_id=user.id)

@router.post("")
@version(1)
async def add_booking(backgroundtasks: BackgroundTasks, room_id: int, date_from: date, date_to: date, user: User = Depends(get_current_user)):
    booking = await BookingService.add_booking(user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to)
    if not booking:
        raise exceptions.RoomCannotBeBooked
    booking_dict = parse_obj_as(BookingSchema, booking).dict()
    # вариант с celery
    # send_booking_confirmation_email.delay(booking_dict, user.email)
    # вариант с встроенной background tasks
    backgroundtasks.add_task(send_booking_confirmation_email, booking_dict, user.email)
    return booking_dict
    