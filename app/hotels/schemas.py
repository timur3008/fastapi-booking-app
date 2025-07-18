from typing import Optional

from pydantic import BaseModel


class HotelSchema(BaseModel):
    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int

    class Config:
        orm_mode = True


class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str] = None
    price: int
    services: Optional[list] = None
    quantity: int
    image_id: int

    class Config:
        orm_mode = True