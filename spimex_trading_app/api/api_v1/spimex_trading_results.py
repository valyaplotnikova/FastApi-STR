from fastapi import APIRouter

router = APIRouter(tags=["Tradings"])


"""
@router.get("/last_trading_dates")
async def get_last_trading_dates(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> list[data]:
    last_trading_dates = await Trading.get_last_trading_dates(session=session)
    return last_trading_dates
    
    
@router.get("/dynamics")
async def get_dynamics(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    last_trading_dates = await Trading.dynamics(session=session)
    return last_trading_dates
    """