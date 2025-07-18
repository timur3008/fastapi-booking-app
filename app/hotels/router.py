import asyncio
from datetime import date

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache
from pydantic import parse_obj_as

from .schemas import HotelSchema, RoomSchema
from .services import HotelService, RoomService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("")
async def get_all_hotels() -> list[HotelSchema]:
    return await HotelService.get_all_items()

@router.get("/rooms")
async def get_all_rooms() -> list[RoomSchema]:
    return await RoomService.get_all_items()

@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location(location: str):
    # await asyncio.sleep(3)
    hotels = await HotelService.get_hotels_by_location(location=location)
    hotels_json = parse_obj_as(list[HotelSchema], hotels)
    return hotels_json

@router.get("/{id}")
async def get_hotel_by_id(id: int) -> HotelSchema:
    return await HotelService.get_by_id(model_id=id)

@router.get("/rooms/{id}")
async def get_room_by_id(id: int) -> RoomSchema:
    return await RoomService.get_by_id(model_id=id)