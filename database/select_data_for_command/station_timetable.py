"""
    Модуль для работы с SELECT запросами к БД.
    Функции модуля предназначенные только для получения информации с БД, таблица 'rus'.
    Логика запросов прописана для команды ТГ-бота: Расписание рейсов по станции.
"""
import aiosqlite
from loguru import logger
from ..CRUD_db import YandexDB
from typing import Optional, Tuple


class Select(YandexDB):

    @staticmethod
    def forming_response(data) -> Optional[str]:
        """
        Метод обрабатывает данные, полученные от запроса к БД.

        Args:
            data: Передает ответ Select запроса к БД.

        Returns: result or None

        """
        transport = {'plane': 'Cамолет', 'train': 'Поезд', 'suburban': 'Электричка', 'water': 'Водный транспорт',
                     'helicopter': 'Вертолет', 'bus': 'Автобус'}
        type_station = {'station': 'Станция', 'platform': 'Платформа', 'stop': 'Остановочный пункт',
                        'checkpoint': 'Блок-пост', 'post': 'Пост', 'crossing': 'Разъезд',
                        'overtaking_point': 'Обгонный пункт', 'train_station': 'Вокзал', 'airport': 'Аэропорт',
                        'bus_station': 'Автовокзал', 'bus_stop': 'Автобусная остановка', 'unknown': 'Станция без типа',
                        'port': 'Порт', 'port_point': 'Портпункт', 'wharf': 'Пристань', 'river_port': 'Речной вокзал',
                        'marine_station': 'Морской вокзал'}
        try:
            result = '<b>Список станций и остановок:</b>\n'
            for title, st_type, tr_type in data:
                tmp = '\n<b>Название станции</b>:\n{name_st}\n<b>Тип</b>: {type}\n' \
                      '<b>Виды транспорта</b>: {transport}\n'.format(name_st=title, type=type_station.get(st_type),
                                                                     transport=transport.get(tr_type, '-'))
                result += tmp
            return result

        except Exception as err:
            logger.error(err)
            return None

    @classmethod
    async def settle(cls, user_msg: str, region_code: str = None) -> Optional[Tuple]:
        """
        Метод класса делает запрос к БД, для получения кода населенного пункта, поле БД CODES_SETTLE
        Args:
            user_msg: Передает название населенного пункта
            region_code: Передает код региона.

        Returns: row or None
        Raises:
            aiosqlite.Error: При ошибки запроса к БД.
        """
        try:
            value = (region_code, f'%{user_msg}%', f'%{user_msg}%')

            query = f"SELECT {cls.CODES_SETTLE}, {cls.TITLE_SETTLE} FROM {cls.TABLE} WHERE {cls.REGION_CODES} LIKE ? " \
                    f"AND ({cls.TITLE_SETTLE} LIKE ? OR {cls.DIRECTION} LIKE ?) " \
                    f"AND {cls.STATION_TYPE} IN ('station', 'train_station', 'bus_station', 'airport', 'bus_stop')"

            cursor = await cls.base.execute(query, value)
            row = await cursor.fetchone()
            return row

        except aiosqlite.Error as err:
            logger.error(err)
            return None

    @classmethod
    async def list_station(cls, settlement_code: str, transport: str) -> Optional[str]:
        """
        Метод класса делает запрос к БД, для получения списка станций населенного пункта.

        Args:
            transport: Передает тип транспортного средства
            settlement_code: Передает код населенного пункта.

        Returns: str or None
        Raises:
            aiosqlite.Error: При ошибки запроса к БД.
        """
        try:
            value = (settlement_code, transport)

            query = f"SELECT {cls.TITLE}, {cls.STATION_TYPE}, {cls.TRANSPORT_TYPE} FROM {cls.TABLE} " \
                    f"WHERE {cls.CODES_SETTLE} LIKE ? AND {cls.TRANSPORT_TYPE} LIKE ?"

            cursor = await cls.base.execute(query, value)
            rows = await cursor.fetchmany(size=30)

        except aiosqlite.Error as err:
            logger.error(err)
            return None

        else:
            return cls.forming_response(data=rows)  # вызываем метод для обработки ответа БД, возвращает str

    @classmethod
    async def yandex_code(cls, user_msg: str, settlement: str, transport_type: str) -> Optional[Tuple]:
        """
        Метод класса делает запрос к БД, для получения яндекс - кода транспортной станции, поле БД YANDEX_CODE.
        Args:
            user_msg: Передает название транспортной станции
            settlement: Передает код населенного пункта
            transport_type: Передает тип транспортного средства.

        Returns: row or None
        Raises:
            aiosqlite.Error: При ошибки запроса к БД.
        """
        logger.info('work')
        try:
            value = (settlement, f'%{user_msg}%', f'%{user_msg}%', transport_type)

            query = f"SELECT {cls.YANDEX_CODE}, {cls.TITLE} FROM {cls.TABLE} WHERE {cls.CODES_SETTLE} LIKE ? " \
                    f"AND ({cls.TITLE} LIKE ? OR {cls.DIRECTION} LIKE ?) AND {cls.TRANSPORT_TYPE} LIKE ?"

            cursor = await cls.base.execute(query, value)
            row = await cursor.fetchone()
            return row

        except aiosqlite.Error as err:
            logger.error(err)
            return None
