import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_image

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)

@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    image_path = f"app/static/images/{name}.webp"
    with open(image_path, mode="wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_image.delay(image_path)