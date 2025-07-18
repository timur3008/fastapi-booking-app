from datetime import date, datetime

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
    (4, "2030-05-01", "2030-05-15", 3, 200),
    (4, "2030-05-01", "2030-05-15", 4, 200),
    (4, "2030-05-01", "2030-05-15", 5, 200),
    (4, "2030-05-01", "2030-05-15", 6, 200),
    (4, "2030-05-01", "2030-05-15", 7, 200),
    (4, "2030-05-01", "2030-05-15", 8, 200),
    (4, "2030-05-01", "2030-05-15", 9, 200),
    (4, "2030-05-01", "2030-05-15", 10, 200),
    (4, "2030-05-01", "2030-05-15", 10, 409),
    (4, "2030-05-01", "2030-05-15", 10, 409),
])
async def test_add_and_get_booking(authenticated_async_client: AsyncClient, room_id, date_from, date_to, booked_rooms, status_code):
    response = await authenticated_async_client.post(
        url="/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    assert response.status_code == status_code

    response = await authenticated_async_client.get("/bookings")
    assert len(response.json()) == booked_rooms