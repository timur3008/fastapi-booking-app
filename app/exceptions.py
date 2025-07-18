from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
)
IncorrectUserDataException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Учётные данные введены неверно"
)
TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не существует"
)
IncorrentTokenFormat = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный формат токена"
)
TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Время токена истёк"
)
UserAbsentException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Не осталось свободных номеров"
)
