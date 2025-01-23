import datetime
from typing import Annotated

from sqlalchemy import func, Float
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class SpimexTradingResults(Base):
    __tablename__ = 'spimex_trading_results'

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[float] = mapped_column(Float, nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    count: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[datetime.date]
    created_on: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_on: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )
