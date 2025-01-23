from fastapi import APIRouter
from api.trading_results.spimex_trading_results import router as trading_router

from core.config import settings

router = APIRouter()
router.include_router(trading_router, prefix=settings.api.smt.trading_results)
