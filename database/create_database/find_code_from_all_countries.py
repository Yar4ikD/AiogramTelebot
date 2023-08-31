import os
import json
from typing import Dict, Any, List
from config import ALL_COUNTRIES_CODE_JSON_PATH
from api.get_all_countries_code import get_code_create_file_json
from .insert_into_db import writing_to_database

""" Этот модуль предназначен для использования как отдельного сценария. """

next_key = None


def get_country(data_dict: Dict, country: str = "Россия") -> None:
    """
    Функция ищет название странны в массиве.
    Принимает 2 аргумента - это массив dict и названия странны.

    Вызывает функцию, для поиска ключей и значений массива, и
    передает аргумент - список регионов, найденной странны,

    :param data_dict: Передает массив данных полный список станций,
                    информацию о которых предоставляют Яндекс Расписания.
    :type data_dict: Dict
    :param country: Передает названия странны, для поиска в массиве.
    """
    for keys in data_dict.get("countries", None):
        if keys.get("title") == country:
            get_regions(keys.get("regions", None))


def get_regions(regions_data: List[Any]) -> None:
    """
    Функция принимает список регионов и проходит циклом по каждому объекту списка.
    На каждом цикле инициализирует словарь для записи ключей и зн-й.
    Объекты списка это словари.
    Извлекает ключи и значения каждого объекта, и записывает их в инициализированный словарь.

    Ищет ключ, значение у которого список населенных пунктов региона.
    Вызывает функцию и передает список населенных пунктов региона, инициализированный словарь
    в качестве аргументов.

    :param regions_data: Передает список регионов.
    :var next_key: Ссылка на список населенных пунктов региона.
    """

    global next_key
    # table_dict = dict()

    for value in regions_data:
        table_dict = dict()

        for key, val in value.items():
            if isinstance(val, list):
                next_key = val

            elif isinstance(val, dict):
                if val.get("yandex_code", None):
                    key = "region_" + key
                    table_dict[key] = val.get("yandex_code")

            else:
                key = "region_" + key
                table_dict[key] = val

        if isinstance(next_key, list):
            get_settlements(next_key, table_dict)


def get_settlements(settle_data: list, columns_table: dict) -> None:
    """
    Функция принимает список населенных пунктов региона и инициализированный словарь.
    Проходит циклом по каждому объекту списка.

    Объекты списка это словари.
    Извлекает ключи и значения каждого объекта, и записывает их в инициализированный словарь.

    Ищет ключ, значение у которого список станций в населенном пункте.
    Вызывает функцию, передает список станций населенного пункта и инициализированный словарь,
    в качестве аргументов.

    :param settle_data: Принимает список населенных пунктов региона.
    :param columns_table: Принимает инициализированный словарь
    :var next_key: Ссылка на список станций
    """
    global next_key

    for value in settle_data:
        for key, val in value.items():
            if isinstance(val, list):
                next_key = val

            elif isinstance(val, dict):
                if val.get("yandex_code", None):
                    key = key + "_settle"
                    columns_table[key] = val.get("yandex_code", None)

            else:
                key = key + "_settle"
                columns_table[key] = val

        if isinstance(next_key, list):
            get_stations(next_key, columns_table)


def get_stations(stations_data: list, columns_table: dict) -> None:
    """
    Функция принимает список станций в населенном пункте и инициализированный словарь.
    Проходит циклом по каждому объекту списка.

    Объекты списка это словари.
    Извлекает ключи и значения каждого объекта, и записывает их в инициализированный словарь.

    Ищет ключ, значение у которого список кодов станции и вызывает функцию,
    передает список станций населенного пункта и инициализированный словарь, в качестве аргументов.

    В конце вызывается функцию из импортированного модуля insert_into_db, для записи данных в БД, которая
    принимает в качестве аргумента инициализированный словарь.

    :param stations_data: Принимает список станций в населенном пункте.
    :param columns_table: Принимает инициализированный словарь
    """
    for value in stations_data:
        for key, val in value.items():
            if isinstance(val, list):
                get_codes(val, columns_table)

            elif isinstance(val, dict):
                for i_key, i_val in val.items():
                    columns_table[i_key] = i_val
            else:
                columns_table[key] = val

        writing_to_database(columns_table)


def get_codes(code_data: list, columns_table: dict) -> None:
    """
    Функция принимает список кодов станции и инициализированный словарь.
    Проходит циклом по каждому объекту списка.

    Объекты списка это словари.
    Извлекает ключи и значения каждого объекта, и записывает их в инициализированный словарь.

    :param code_data: Принимает список кодов станции.
    :param columns_table: Принимает инициализированный словарь.

    """
    for value in code_data:
        for key, val in value.items():
            columns_table[key] = val


def main():
    if not os.path.exists(ALL_COUNTRIES_CODE_JSON_PATH):
        get_code_create_file_json(ALL_COUNTRIES_CODE_JSON_PATH)

    with open(ALL_COUNTRIES_CODE_JSON_PATH, "r") as file:
        print("Запись в БД...")
        data = json.load(file)
        get_country(data)

    print("Загрузка БД завершена!")


if __name__ == "__main__":
    main()
