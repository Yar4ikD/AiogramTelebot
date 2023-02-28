"""
    Модуль для работы с SELECT запросами к БД.
    Функции модуля предназначенные только для получения информации с БД, таблица 'rus'.
    Логика запросов прописана для команды ТГ-бота: Расписание рейсов между станциями.
"""

import aiosqlite
from loguru import logger
from ..codes_db import YandexDB
from typing import Tuple, Optional


class Select(YandexDB):

    @classmethod
    async def region(cls, user_msg: str) -> Optional[Tuple]:
        return await cls.select_region(user_msg)

    @classmethod
    async def settle(cls, user_msg: str, region_code: str = None) -> Optional[Tuple]:
        """
        Метод класса делает запрос к БД, для получения кода населенного пункта, поле БД CODES_SETTLE

        Args:
            user_msg: Передает название населенного пункта
            region_code: Передает код региона.

        Returns: str or None
        Raises:
            aiosqlite.Error: При ошибки запроса к БД.

        """
        try:
            value = (region_code, f'%{user_msg}%', f'%{user_msg}%')

            query = f"SELECT {cls.CODES_SETTLE}, {cls.TITLE_SETTLE} FROM {cls.TABLE} WHERE {cls.REGION_CODES} LIKE ? " \
                    f"AND ({cls.TITLE_SETTLE} LIKE ? OR {cls.DIRECTION} LIKE ?) " \
                    f"AND {cls.STATION_TYPE} IN ('station', 'train_station', 'bus_station', 'airport')"

            cursor = await cls.base.execute(query, value)
            row = await cursor.fetchone()
            return row

        except aiosqlite.Error as err:
            logger.exception(err)
            return None
