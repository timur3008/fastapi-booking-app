import pytest

from app.users.services import UserService


@pytest.mark.parametrize("user_id,email,exists", [
    (1, "tboltaboyev123@gmail.com", True),
    (2, "eliseysilovich007@gmail.com", True),
    (5, ".......", False)
])
async def test_find_user_by_id(user_id: int, email: str, exists: bool):
    user = await UserService.get_by_id(user_id) 
    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user