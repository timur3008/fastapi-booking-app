import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("eliseysilovich007@gmail.com", "@qwerty123", 200),
    ("eliseysilovich007@gmail.com", "@qwerty1234", 409),
    ("endreysilovich127@gmail.com", "@qwerty1234", 200),
    ("abcde", "@qwerty1234", 422)
])
async def test_register_user(email: str, password: str, status_code: int, async_client: AsyncClient):
    response = await async_client.post(
        "/auth/register", 
        json={"email": email, "password": password}
    )
    assert response.status_code == status_code

@pytest.mark.parametrize("email,password,status_code", [
    ("tboltaboyev123@gmail.com", "@qwerty123", 200),
    ("eliseysilovich007@gmail.com", "@qwerty123", 200),
    # ("wrong@user.com", "@qwerty123", 401)
])
async def test_login_user(email: str, password: str, status_code: int, async_client: AsyncClient):
    response = await async_client.post(
        "auth/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == status_code