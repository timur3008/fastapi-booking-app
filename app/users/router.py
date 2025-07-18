from fastapi import APIRouter, Depends, HTTPException, Response, status

from app import exceptions

from .auth import authenticate_user, create_access_token, get_password_hash
from .dependencies import get_current_user
from .models import User
from .services import UserService
from .shemas import UserAuthSchema

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(user_data: UserAuthSchema):
    user_exists = await UserService.get_one_or_none(email=user_data.email)
    if user_exists:
        raise exceptions.UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserService.add_data(email=user_data.email, hashed_password=hashed_password)
    
@router.post("/login")
async def login_user(response: Response, user_data: UserAuthSchema):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if not user:
        raise exceptions.IncorrectUserDataException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return {"detail": status.HTTP_200_OK}

@router.get("/me")
async def get_users_me(current_user: User = Depends(get_current_user)):
    return current_user