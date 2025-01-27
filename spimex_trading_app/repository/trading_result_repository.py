from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence

from sqlalchemy import insert, select

from core.models import SpimexTradingResults
from filters.trading_filters import SpimexTradingResultsFilter


class AbstractRepository(ABC):

    @abstractmethod
    async def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    model = None

    def __init__(self, session):
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(self.model).values(**kwargs)
        await self.session.execute(query)

    async def get(self, reference):
        return self.session.query(self.model).filter_by(reference=reference).one()


class SpimexTradingResultsRepository(SqlAlchemyRepository):

    model = SpimexTradingResults

    async def get_last_trading_dates(self, days: int) -> list[datetime.date]:
        """
        Получает список дат последних торговых дней

        :param days: количество дней, за которые нужно полученить даты торгов
        :return: list[datetime.date] список дат последних торговых дней
        """
        stmt = select(self.model.date).distinct().order_by(self.model.date.desc()).limit(days)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_dynamics(self, start_date, end_date, str_filter: SpimexTradingResultsFilter) -> Sequence[type(model)]:
        """
        Получает список торгов за заданный период.

        :param start_date: Дата в формате 'YYYY-MM-DD', начиная с которой нужно получить список торгов.
        :param end_date: Дата в формате 'YYYY-MM-DD', заканчивая которой нужно получить список торгов.
        :param str_filter: Объект фильтра типа SpimexTradingResultsFilter, содержащий параметры фильтрации данных.

        :return: Список торгов за указанный период, отсортированный по дате.
                 Возвращает последовательность объектов модели, соответствующих заданным критериям.
        """
        # start_date = datetime.strptime(start_date, '%Y-%m-%d')
        # end_date = datetime.strptime(end_date, '%Y-%m-%d')
        query = str_filter.filter(select(self.model).where(self.model.date.between(start_date, end_date)))
        result = await self.session.execute(query.order_by(self.model.date))
        return result.scalars().all()

    async def get_trading_results(self, str_filter: SpimexTradingResultsFilter) -> Sequence[type(model)]:
        """
        Получает список последних торгов.

        :param str_filter: Объект фильтра типа SpimexTradingResultsFilter, содержащий параметры фильтрации данных.
        :return: Список последних торгов, отсортированный по дате.
             Возвращает последовательность объектов модели, соответствующих заданным критериям.
        """
        query = str_filter.filter(select(self.model))
        result = await self.session.execute(query.order_by(self.model.date.desc()).limit(1))
        return result.scalars().all()
