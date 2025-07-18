from sqladmin import ModelView

from app.bookings.models import Booking
from app.hotels.models import Hotel, Room
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password]

    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingAdmin(ModelView, model=Booking):
    column_list = [table.name for table in Booking.__table__.c] + [Booking.user, Booking.room]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"


class HotelAdmin(ModelView, model=Hotel):
    column_list = [table.name for table in Hotel.__table__.c]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomAdmin(ModelView, model=Room):
    column_list = [table.name for table in Room.__table__.c] + [Room.hotel]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"