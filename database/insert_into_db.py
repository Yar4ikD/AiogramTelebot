from create_db import YandexDB
from typing import Dict

columns: str = ''


def writing_to_database(data_code: Dict, name_tb: str = 'rus') -> None:
    """
    Функция создает и записывает данные в БД.

    :param data_code: Передает данные для записи в БД.
    :param name_tb: Передает имя БД.
    :var db: Экземпляр класса, инициализирует и производит подключение к конкретной БД.
    """
    global columns
    db = YandexDB('RusCode')

    if not len(columns):
        columns = ', '.join(x for x in data_code.keys())
        table = '{name} ({colum})'.format(name=name_tb, colum=columns)
        db.add_table(table)

    if all(x in columns for x in data_code.keys()):
        data_row = tuple(data_code.get(key) for key in columns.split(', '))

    else:
        new_column = ''.join(key for key in data_code.keys() if key not in columns)
        db.add_column(name_tb, new_column)
        columns = ', '.join(x for x in data_code.keys())
        data_row = tuple(data_code.get(key) for key in columns.split(', '))

    db.insert_data(name_tb, data_row)
