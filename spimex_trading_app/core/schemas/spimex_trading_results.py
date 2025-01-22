import datetime

from pydantic import BaseModel, Field


class SpimexTradingResultsSchema(BaseModel):
    """
    Схема для валидации данных
    """

    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: str = Field(default="-")
    total: str = Field(default="-")
    count: str = Field(default="-")
    date: datetime.date
