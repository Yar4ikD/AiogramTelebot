import sqlite3 as sq
import aiosqlite
from typing import List, Tuple, Optional
from config import DB_PATH

"""
Модуль для работы с БД.
СУБД - SQLite3
"""


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

        :param name_db: Передает имя файла БД, по умолчанию "code_rus".
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
        query = f"CREATE TABLE IF NOT EXISTS {table}"
        self.__cur.execute(query)
        self.__base.commit()

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
    async def select_region_or_settlement(cls, user_msg: str, type_query: str, table: str = TABLE):

        query = None
        if type_query == 'region':

            query = f"""SELECT {cls.REGION_CODES}, {cls.REGION_TITLE} FROM {table} 
            WHERE {cls.REGION_TITLE} LIKE '{user_msg}%' OR {cls.REGION_TITLE} LIKE '%{user_msg}' 
            """

        elif type_query == 'settlement':
            query = f"SELECT {cls.CODES_SETTLE}, {cls.TITLE_SETTLE} FROM {table} " \
                    f"WHERE {cls.TITLE_SETTLE} LIKE '%{user_msg}%' OR {cls.DIRECTION} LIKE '%{user_msg}%' " \
                    f"AND ({cls.STATION_TYPE} LIKE 'station' OR {cls.STATION_TYPE} LIKE 'train_station' " \
                    f"OR {cls.STATION_TYPE} LIKE 'bus_station' OR {cls.STATION_TYPE} LIKE 'airport')"
        else:
            return None

        cursor = await cls.base.execute(query)
        row = await cursor.fetchone()
        return row

    @classmethod
    async def select_list_station(cls, region_code: str, settlement_code: str, table: str = TABLE, limit=None):

        query = f'SELECT {cls.TITLE}, {cls.STATION_TYPE}, {cls.TRANSPORT_TYPE} FROM {table} WHERE ' \
                f'({cls.REGION_CODES} = "{region_code}" AND {cls.CODES_SETTLE} = "{settlement_code}") ' \
                f'AND ({cls.STATION_TYPE} LIKE "station" OR {cls.STATION_TYPE} LIKE "train_station" ' \
                f'OR {cls.STATION_TYPE} LIKE "bus_station" OR {cls.STATION_TYPE} LIKE "airport")'

        cursor = await cls.base.execute(query)
        rows = await cursor.fetchmany(size=15)

        return rows

    @classmethod
    async def select_yandex_code(cls, user_msg: str, region: str, settlement: str, table: str = TABLE, limit: int = 10):

        query = f"""
        SELECT {cls.YANDEX_CODE}, {cls.TITLE} FROM {table} WHERE {cls.REGION_CODES} LIKE '{region}' 
        AND {cls.CODES_SETTLE} LIKE '{settlement}' AND {cls.TITLE} LIKE '%{user_msg}%' 
        LIMIT {limit}
        """

        cursor = await cls.base.execute(query)
        row = await cursor.fetchone()
        print(row)
        return row

