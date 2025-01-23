from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from filters.trading_filters import SpimexTradingResultsFilter
from repository.trading_result_repository import SpimexTradingResultsRepository

router = APIRouter(tags=["Tradings"])


@router.get("/last_trading_dates/{days}")
@cache(expire=3600 * 24)
async def get_last_trading_dates(session: Annotated[AsyncSession, Depends(db_helper.session_getter),], days: int):
    last_trading_dates = await SpimexTradingResultsRepository(session=session).get_last_trading_dates(days)
    return last_trading_dates
    

@router.get("/dynamics")
@cache(expire=3600 * 24)
async def get_dynamics(
        start_date,
        end_date,
        str_filter: Annotated[SpimexTradingResultsFilter, Depends(SpimexTradingResultsFilter)],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    last_trading_dates = await SpimexTradingResultsRepository(session=session).get_dynamics(
        start_date, end_date, str_filter
    )
    return last_trading_dates


@router.get("/last_tradings")
@cache(expire=3600 * 24)
async def get_last_trading(
        str_filter: Annotated[SpimexTradingResultsFilter, Depends(SpimexTradingResultsFilter)],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    last_tradings = await SpimexTradingResultsRepository(session=session).get_trading_results(str_filter)
    return last_tradings
