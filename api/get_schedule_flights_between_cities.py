"""
    В данном модуле прописана логика работы,
    для получения списка рейсов, следующих от указанного населенного пункта отправления
    к указанному населенному пункту прибытия и информацию, по каждому рейсу от API Яндекс Расписаний,
    раздел Расписание рейсов между станциями
"""

import emoji
from datetime import datetime, timedelta
from config import YANDEX_API_KEY
from typing import Dict, Optional
from .base_get_requests import get_request
from loguru import logger


async def request(
    from_city: str, to_city: str, transport_type: str, date: str
) -> Optional[str]:
    """
    Функция создает параметры для запроса к API Расписание рейсов между станциями(словарь) из полученных аргументов.
    Вызывает функцию get_request, модуля base_get_requests и передает в качестве аргументов переменные:
    params(словарь) и url. Переменная url - это адрес GET-запроса к API Яндекс Расписаний.

    Если результат функции get_request - None, возвращает None

    Если результат функции get_request - not None, возвращает результат работы функции forming_response,
    с передачей ей в качестве аргумента результат функции get_request.

    Args:
        from_city: Передает код населенного пункта отправления.
        to_city: Передает код населенного пункта прибытия.
        transport_type: Передает тип транспортного средства.
        date: Передает дату, на которую необходимо получить список рейсов. YYYY-MM-DD

    Returns: forming_response or None

    """
    params = {
        "apikey": YANDEX_API_KEY,
        "format": "json",
        "from": from_city,
        "to": to_city,
        "transport_types": transport_type,
        "date": date,
        "limit": 10,
    }

    url = "https://api.rasp.yandex.net/v3.0/search/"

    result = await get_request(url=url, params=params)

    if result:
        return forming_response(data=result)

    return None


def forming_response(data: Dict) -> Optional[str]:
    """
    Функция извлекает и структурирует информацию. Принимает аргумент - словарь.
    В словаре данные полученные из GET запроса к API Яндекс Расписаний, раздел - Расписание рейсов между станциями.
    Возвращает строку структурированных данных, или None если отсутствуют ключи в словаре.

    Args:
        data: Передает данные, полученные из GET запроса к API Яндекс, раздел - Расписание рейсов между станциями.

    Returns: result
    Raises:
        Exception: При ошибке работе цикла

    """
    result = None

    try:
        if data.get("segments"):
            result = f'Найденная информация{emoji.emojize(":information:")}'
            for value in data.get("segments"):
                result += check_data("\nНомер рейса: ", value, "thread", "number")

                result += "\nОтправления:\n"
                result += check_data("Пункт: ", value, "from", "title")
                result += check_data("Платформа: ", value, "departure_platform")
                result += check_data("Терминал: ", value, "departure_terminal")
                result += check_data("Время: ", value, "departure")

                result += "\nПрибытия:\n"
                result += check_data("Станция: ", value, "to", "title")
                result += check_data("Платформа: ", value, "arrival_platform")
                result += check_data("Терминал: ", value, "arrival_terminal")
                result += check_data("Время: ", value, "arrival")

                if value.get("has_transfers"):
                    result += "Наличия пересадок по ходу рейса!\n"

                result += check_data("Продолжительность рейса: ", value, "duration")

                flag = (
                    "Возможно."
                    if value.get("tickets_info", {}).get("et_marker")
                    else "Нет"
                )
                result += "Купить электронный билет: {}\n".format(flag)
                result += check_data(
                    "Транспортное средство:\n", value, "thread", "vehicle"
                )

                result += check_data(
                    "Перевозчик: ", value, "thread", "carrier", "title"
                )
                result += check_data(
                    "Номер телефона:\n", value, "thread", "carrier", "phone"
                )
                result += check_data("Сайт:\n", value, "thread", "carrier", "url")
                result += "-" * 30

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
        if get_data.get(key_1, {}).get(key_2, {}).get(key_3):
            data = get_data.get(key_1).get(key_2).get(key_3)
            return text + data + "\n"

    elif key_1 and key_2:
        if get_data.get(key_1, {}).get(key_2):
            data = get_data.get(key_1).get(key_2)
            return text + data + "\n"

    else:
        if get_data.get(key_1):
            data = get_data.get(key_1)

            if key_1 == "duration":
                data = f"{(int(data) // 60)} мин."

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
