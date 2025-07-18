from datetime import datetime

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app import exceptions
from app.config import settings

from .services import UserService


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise exceptions.TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise exceptions.IncorrentTokenFormat
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise exceptions.TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise exceptions.UserAbsentException
    user = await UserService.get_by_id(int(user_id))
    if not user:
        raise exceptions.UserAbsentException
    return user