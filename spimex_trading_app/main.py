from contextlib import asynccontextmanager

from fastapi import FastAPI

# from fastapi.responses import ORJSONResponse

from core.config import settings

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from api import router as api_router
from core.models import db_helper
from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    redis = aioredis.from_url(f"{settings.celery.broker}://{settings.celery.port}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    # shutdown
    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan,
    # default_response_class=ORJSONResponse,
)

main_app.include_router(
    api_router,
    prefix=settings.api.prefix,
)
