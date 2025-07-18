from celery import Celery

from app.config import settings

celery = Celery("tasks", broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", include=["app.tasks.tasks"])

# TODO
# celery -A app.tasks.celery:celery worker --loglevel=INFO --pool=solo