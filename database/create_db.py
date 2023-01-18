import sqlite3 as sq

"""
Модуль для создания БД и работы с ней.
СУБД - SQLite3
"""


class YandexDB:

    def __init__(self, name_db: str = 'code_rus') -> None:
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
