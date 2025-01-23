import asyncio
import datetime
import re
from typing import Optional
from urllib.parse import urljoin

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import settings
from core.models import SpimexTradingResults


class Parser:
    def __init__(self) -> None:
        self.base_url = 'https://spimex.com/markets/oil_products/trades/results/'
        self.engine = create_async_engine(str(settings.db.url), future=True, echo=True)
        self.async_session = async_sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    @staticmethod
    async def fetch(session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """
        Загружает содержимое страницы по указанному URL.
        :param session: Сессия aiohttp для выполнения запросов.
        :param url: URL страницы, которую нужно загрузить.
        :return: Содержимое страницы в виде строки или None в случае ошибки.
        """
        try:
            async with session.get(url) as response:
                response.raise_for_status()  # Вызывает исключение для статусов 4xx/5xx
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Ошибка при загрузке страницы {url}: {e}")
            return None

    @staticmethod
    async def get_data_from_excel(file_content: bytes, trade_date: datetime.date) -> Optional[pd.DataFrame]:
        """
        Загружает данные из Excel-файла и возвращает DataFrame с нужной структурой.
        :param file_content: Содержимое Excel-файла в байтовом формате.
        :param trade_date: Дата торговли.
        :return: DataFrame с данными торговли или None, если данные отсутствуют.
        """
        from io import BytesIO

        try:
            temp_df = pd.read_excel(BytesIO(file_content), header=None)
        except Exception as e:
            print(f"Ошибка при чтении Excel-файла: {e}")
            return None

        # Поиск строки, где начинается нужная информация
        row_start = temp_df[temp_df.apply(
            lambda x: x.astype(str).str.contains('Единица измерения: Метрическая тонна', na=False).any(), axis=1
        )].index
        if row_start.empty:
            print("Не удалось найти строку с 'Единица измерения: Метрическая тонна'")
            return None
        row_start = row_start[0]

        header_row = row_start + 1
        df = pd.read_excel(BytesIO(file_content), header=header_row)

        # Преобразование типов
        df['Количество\nДоговоров,\nшт.'] = pd.to_numeric(df['Количество\nДоговоров,\nшт.'], errors='coerce')

        filtered_data = df[
            (df['Количество\nДоговоров,\nшт.'] > 0) &
            (df['Наименование\nИнструмента'].notna())
        ]

        if filtered_data.empty:
            print("Нет данных для сохранения в базу данных.")
            return None

        # Создание нового DataFrame с нужной структурой
        spimex_trading_results = pd.DataFrame({
            'exchange_product_id': filtered_data['Код\nИнструмента'],
            'exchange_product_name': filtered_data['Наименование\nИнструмента'],
            'oil_id': filtered_data['Код\nИнструмента'].str[:4],
            'delivery_basis_id': filtered_data['Код\nИнструмента'].str[4:7],
            'delivery_basis_name': filtered_data['Базис\nпоставки'],
            'delivery_type_id': filtered_data['Код\nИнструмента'].str[-1],
            'volume': pd.to_numeric(filtered_data['Объем\nДоговоров\nв единицах\nизмерения']),
            'total': pd.to_numeric(filtered_data['Обьем\nДоговоров,\nруб.']),
            'count': pd.to_numeric(filtered_data['Количество\nДоговоров,\nшт.']),
            'date': trade_date,
            'created_on': pd.to_datetime('now'),
            'updated_on': pd.to_datetime('now')
        })

        print('Данные готовы для сохранения в базу данных')
        return spimex_trading_results

    async def save_data_to_db(self, spimex_trading_results: pd.DataFrame) -> None:
        """
        Сохраняет данные из DataFrame в базу данных.
        :param spimex_trading_results: DataFrame с данными торговли для сохранения.
        """
        async with self.async_session() as session:
            async with session.begin():
                try:
                    for index, row in spimex_trading_results.iterrows():
                        result = SpimexTradingResults(
                            exchange_product_id=row['exchange_product_id'],
                            exchange_product_name=row['exchange_product_name'],
                            oil_id=row['oil_id'],
                            delivery_basis_id=row['delivery_basis_id'],
                            delivery_basis_name=row['delivery_basis_name'],
                            delivery_type_id=row['delivery_type_id'],
                            volume=row['volume'],
                            total=row['total'],
                            count=row['count'],
                            date=row['date'],
                            created_on=row['created_on'],
                            updated_on=row['updated_on']
                        )
                        session.add(result)

                    await session.commit()  # Коммитим все изменения после добавления всех объектов
                    print('Данные успешно сохранены в базу данных')
                except Exception as e:
                    await session.rollback()  # Откат изменений в случае ошибки
                    print(f"Ошибка при сохранении данных в базу данных: {e}")

    async def get_trading_all_dates_and_files(self, queue: asyncio.Queue) -> None:
        """
        Извлекает все даты торгов и соответствующие ссылки на файлы с сайта,
        добавляя их в асинхронную очередь.

        :param queue: Асинхронная очередь для хранения ссылок на файлы.
        """
        page_number = 1

        async with aiohttp.ClientSession() as session:
            while True:
                response = await self.fetch(session, f"{self.base_url}?page=page-{page_number}")

                if response:
                    soup = BeautifulSoup(response, 'html.parser')

                    link_tags = soup.find_all('a', class_='accordeon-inner__item-title link xls')
                    if not link_tags:
                        print(f"На странице {page_number} нет ссылок на файлы.")
                        break

                    for link_tag in link_tags:
                        file_link = link_tag['href']
                        if not file_link.startswith('http'):
                            file_link = urljoin(self.base_url, file_link)
                        match = re.search(r'_(\d{14})\.xls', file_link)
                        if match:
                            date_str = match.group(1)
                            trade_date = datetime.datetime.strptime(date_str, '%Y%m%d%H%M%S').date()
                            if trade_date >= datetime.datetime(2023, 1, 1).date():
                                await queue.put((trade_date, file_link))  # Добавляем в очередь
                            else:
                                break

                    # Проверка на наличие следующей страницы
                    next_page = soup.select_one('.bx-pag-next a')
                    if next_page:
                        next_page_url = next_page['href']
                        match = re.search(r'page=page-(\d+)', next_page_url)
                        if match:
                            page_number = int(match.group(1))  # Переходим к следующей странице
                            print(f"Переход на страницу {page_number}...")
                        else:
                            print("Не удалось извлечь номер следующей страницы.")
                            break
                    else:
                        print("Следующая страница не найдена.")
                        break
                else:
                    break

    async def process_files(self, queue: asyncio.Queue) -> None:
        """
        Асинхронно обрабатывает скачивание файлов и сохранение данных в БД.
        :param queue: Асинхронная очередь для получения ссылок на файлы и дат торговли.
        """
        async with aiohttp.ClientSession() as session:
            while True:
                trade_date, link = await queue.get()  # Получаем ссылку из очереди
                if link is None:  # Если получена сигнальная метка завершения
                    break
                try:
                    async with session.get(link) as file_response:
                        file_response.raise_for_status()  # Проверка на статус ответа
                        file_content = await file_response.read()  # Читаем содержимое файла
                        spimex_trading_results = await self.get_data_from_excel(file_content, trade_date)
                        if spimex_trading_results is not None:
                            await self.save_data_to_db(spimex_trading_results)  # Сохраняем данные в БД
                except Exception as e:
                    print(f"Ошибка при обработке файла {link}: {e}")


async def main():
    """
    Основная функция, которая запускает асинхронные задачи для извлечения ссылок на файлы
    и загрузки данных в базу данных.
    """
    parser = Parser()
    queue = asyncio.Queue()

    # Запускаем задачи для загрузки файлов
    processing_task = asyncio.create_task(parser.process_files(queue))

    # Запускаем задачу для извлечения ссылок на файлы
    await parser.get_trading_all_dates_and_files(queue)

    # Завершаем задачу обработки
    await queue.put((None, None))  # Отправляем сигнальную метку завершения
    await processing_task  # Ждем завершения обработки

if __name__ == "__main__":
    asyncio.run(main())
