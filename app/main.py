import time
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.admin.auth import authenticationbackend
from app.admin.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.bookings.router import router as bookings_router
from app.database import engine
from app.files.router import router as images_router
from app.hotels.router import router as hotels_router
from app.pages.router import router as router_pages
from app.users.router import router as users_router
from app.logger import logger


sentry_sdk.init(
    dsn="https://3069c8ea518810a85311728aefe7fd02@o4509688551768064.ingest.us.sentry.io/4509688553996288",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)


app = FastAPI()

app = VersionedFastAPI(
    app=app, 
    version_format="{major}",
    prefix_format="/v{major}",
    # description="Greet users with a nice message"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
admin = Admin(app=app, engine=engine, authentication_backend=authenticationbackend)

admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(router_pages)
app.include_router(images_router)

origins = ["http://localhost:3000"] # площадки которые могут обращаться к api

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Authorization"]
)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)
instrumentator.instrument(app).expose(app)

@app.middleware("http")
async def add_process_time_handler(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # response.headers["X-Process-Time"] = str(process_time)
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response


# pip install black flake8 autoflake isort pyright
# Black — библиотека, которая автоматически форматирует код, приводя его внешний
# вид к стандарту PEP 8
# Flake8 — инструмент, позволяющий просканировать код проекта и обнаружить в
# нем стилистические ошибки и нарушения различных конвенций кода на Python
# isort — библиотека Python для сортировки импорта по алфавиту с автоматическим
# разделением на разделы и по типам
# autoflake — утилита помогает удалить не используемые импорты и переменные
# pyright — быстрая статическая проверка типов и валидатор кода
# 
# black <file_path> --diff --color - узнать как правильно
# black <file_path> - отформатировать
# 
# flake8 <file_path> - показывает где у нас могут быть ошибки
# 
# isort <file_path> -rc - сортирует импорты рекурсивно
# 
# autoflake <file_path>
# pyright <file_path>
# 
# #