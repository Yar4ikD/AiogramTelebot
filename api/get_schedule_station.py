"""
    Модуль для работы с GET-запросами.
    Запрос к API - Расписание рейсов по станции.
"""

from datetime import datetime, timedelta
from loguru import logger
from config import YANDEX_API_KEY
from typing import Dict, Optional
from .base_get_requests import get_request


async def request(
    station_code: str,
    date=datetime.today(),
    transport: str = "suburban",
    event: str = "arrival",
) -> Optional[str]:
    """
    Функция создает параметры для GET запроса, API Расписание рейсов по станции(словарь), из полученных аргументов.
    Вызывает функцию get_request, модуля base_get_requests и передает в качестве аргументов переменные:
    params(словарь) и url. Переменная url - это адрес GET-запроса к API Яндекс Расписаний.

    Если результат функции get_request - None, возвращает None

    Если результат функции get_request - not None, возвращает результат работы функции forming_response,
    с передачей ей в качестве аргумента результат функции get_request.
    Args:
        station_code: Передает код станции в населенном пункте
        date: Передает дату
        transport: Передает тип транспорта
        event: Передает направление транспорта со станции

    Returns: forming_response or None

    """
    params = {
        "apikey": YANDEX_API_KEY,
        "station": station_code,
        "format": "json",
        "date": date,
        "transport_types": transport,
        "event": event,
        "direction": "all",
    }
    url = "https://api.rasp.yandex.net/v3.0/schedule/"
    result = await get_request(url=url, params=params)

    if result:
        return forming_response(data=result)
    return None


def forming_response(data: Dict) -> Optional[str]:
    """
    Функция извлекает и структурирует информацию. Принимает аргумент - словарь.
    В словаре данные полученные из GET запроса к API Яндекс Расписаний, раздел - Расписание рейсов по станции.
    Возвращает строку структурированных данных, или None если отсутствуют ключи в словаре.

    Args:
        data: Передает данные, полученные из GET запроса.

    Returns: result
    Raises:
        Exception: При ошибке работе цикла

    """
    limit = 20
    result = None

    try:
        result = check_data("Станция: ", data, "station", "title")
        result += check_data("Тип станции: ", data, "station", "station_type_name")
        result += check_data("Дата: ", data, "date")

        for count, value in enumerate(data.get("schedule")):
            if count >= limit:
                break
            result += check_data("\nНазвание нитки:\n", value, "thread", "title")
            result += check_data("Номер рейса: ", value, "thread", "number")
            result += check_data("Терминал аэропорта: ", value, "terminal")
            result += check_data("Платформа отправления:\n", value, "platform")
            result += check_data("Время отправления:\n", value, "departure")
            result += check_data("Время прибытия:\n", value, "arrival")
            result += check_data("Дни курсирования: ", value, "days")

            # result += check_data('Перевозчик: ', value, 'thread', 'carrier', 'title')
            result += check_data("Транспортное средство: ", value, "thread", "vehicle")
            result += check_data("", value, "thread", "transport_subtype", "title")

        return result

    except Exception as err:
        logger.exception(err)
        return None


def check_data(
    text: str, get_data: Dict, key_1: str = None, key_2: str = None, key_3: str = None
) -> str:
    """
    Функция проверки данных словаря.

    Args:
        key_3: Передает ключ словаря
        key_2: Передает ключ словаря
        key_1: Передает ключ словаря
        text: Передает строку
        get_data: Передает словарь с данными

    Returns: text + get_data or ''

    """
    if key_1 and key_2 and key_3:
        if get_data.get(key_1, {}).get(key_2, {}).get(key_3, None):
            data = get_data.get(key_1).get(key_2).get(key_3)
            return text + data + "\n"

    elif key_1 and key_2:
        if get_data.get(key_1, {}).get(key_2):
            data = get_data.get(key_1).get(key_2)
            return text + data + "\n"

    else:
        if get_data.get(key_1):
            data = get_data.get(key_1)

            if key_1 in ("departure", "arrival"):
                data = data.split("+")

                if len(data) == 2:
                    tmp_t_zone, tmp_t_delta = data[0], data[1].split(":")
                    normal_date = datetime.fromisoformat(tmp_t_zone)
                    data = normal_date + timedelta(
                        hours=int(tmp_t_delta[0]), minutes=int(tmp_t_delta[1])
                    )

                else:
                    data = datetime.fromisoformat(data[0])

            return text + str(data) + "\n"

    return ""
