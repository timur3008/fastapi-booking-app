import asyncio
import json
from datetime import datetime

import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.bookings.models import Booking
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.hotels.models import Hotel, Room
from app.main import app as fastapi_app
from app.users.models import User


@pytest.fixture(scope="session", autouse=True) # подготавливает определённую среду для тестирования
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", mode="r", encoding="utf-8") as file:
            return json.load(file)
        
    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = sa.insert(Hotel).values(hotels)
        add_rooms = sa.insert(Room).values(rooms)
        add_users = sa.insert(User).values(users)
        add_bookings = sa.insert(Booking).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def authenticated_async_client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/auth/login", json={"email": "tboltaboyev123@gmail.com", "password": "@qwerty123"})
        assert ac.cookies["booking_access_token"]
        yield ac

@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session