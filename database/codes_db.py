"""
    Модуль для работы с БД.
    СУБД - SQLite3
"""

import sqlite3 as sq
import aiosqlite
from typing import Tuple, Optional
from loguru import logger
from config import DB_PATH


class YandexDB:

    TABLE = 'rus'
    REGION_TITLE = 'region_title'
    REGION_CODES = 'region_codes'
    TITLE_SETTLE = 'title_settle'
    CODES_SETTLE = 'codes_settle'
    DIRECTION = 'direction'
    TITLE = 'title'
    STATION_TYPE = 'station_type'
    TRANSPORT_TYPE = 'transport_type'
    YANDEX_CODE = 'yandex_code'
    name_db = DB_PATH
    base = None

    def __init__(self, name_db: str = 'RusCode') -> None:
        """
        Магический метод класса, инициализирует БД.
        Создает БД с расширением db и производится подключение к конкретной БД.
        Создается курсор из соединения с БД

        :param name_db: Передает имя файла БД, по умолчанию "code_rus"
        :type name_db: str
        """
        if name_db.endswith('.db'):
            self.name = name_db
        else:
            self.name = name_db + '.db'

        with sq.connect(self.name) as con:  # производится подключение к БД
            self.__cur = con.cursor()  # Создается курсор из соединения с БД
            self.__base = con  # соединения с БД

    @classmethod
    async def connect_db(cls) -> None:
        cls.base = await aiosqlite.connect(cls.name_db)

    def add_table(self, table: str = 'user (?, ?, ?)') -> None:
        """
        Метод класса, создает таблицу БД.

        :param table: Передает имя таблицы
        """
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table}"
            self.__cur.execute(query)
            self.__base.commit()
        except sq.Error as err:
            logger.exception(err)

    def insert_data(self, table: str, data: tuple) -> None:
        """
        Метод класса записывает данные в таблицу БД.

        :param table: Передает имя таблицы, в которую производится запись.
        :param data: Передает данные для записи в таблицу БД.
        :rtype data: Tuple[Any]
        """
        if len(data) > 1:
            symbol = ', '.join('?' * len(data))
            query = f"INSERT INTO {table} VALUES ({symbol})"

        else:
            query = f"INSERT INTO {table} VALUES (?)"

        self.__cur.execute(query, data)
        self.__base.commit()

    def add_column(self, name_tb: str, name_column) -> None:
        """
        Метод класса добавляет поле в таблицу БД.

        :param name_tb: Передает имя таблицы, в которой производится запись.
        :param name_column: Передает имя поля, которое будет добавлено в таблицу БД.
        """
        query = f"ALTER TABLE {name_tb} ADD COLUMN {name_column}"
        self.__cur.execute(query)
        self.__base.commit()

    def delete_table(self, name_tb) -> None:
        """
        Метод класса удаляет таблицу БД.

        :param name_tb: Передает имя таблицы, которую нужно удалить.
        """
        query = f"DROP TABLE IF EXISTS {name_tb}"
        self.__cur.execute(query)
        self.__base.commit()

    @classmethod
    async def select_region(cls, user_msg: str) -> Optional[Tuple]:
        """
        Метод класса делает запрос к БД, для получения кода региона, поле БД REGION_CODES
        Args:
            user_msg: Передает название региона.

        Returns: row
        Raises:
            aiosqlite.Error: При ошибки запроса к БД.
        """
        try:
            table = cls.TABLE
            value = (f'%{user_msg}%', f'%{user_msg}')
            query = f"SELECT {cls.REGION_CODES}, {cls.REGION_TITLE} FROM {table} " \
                    f"WHERE {cls.REGION_TITLE} LIKE ? OR {cls.REGION_TITLE} LIKE ?"

            cursor = await cls.base.execute(query, value)
            row = await cursor.fetchone()
            return row

        except aiosqlite.Error as err:
            logger.exception(err)
            return None
