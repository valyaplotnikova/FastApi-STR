from celery import Celery
from celery.schedules import crontab
from fastapi_cache import FastAPICache

from core.config import settings

celery_app = Celery(
    'tasks',
    broker=f'{settings.celery.broker}://{settings.celery.broker}:{settings.celery.port}',
    backend=f'{settings.celery.broker}://{settings.celery.broker}:{settings.celery.port}'
)


@celery_app.task
def clear_cache():
    FastAPICache.clear()
    print("Cache cleared!")


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='14', minute='11'), clear_cache.s(), name='Clear cache every day at 14:11')
