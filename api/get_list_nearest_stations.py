"""
    Модуль для работы с GET-запросами.
    Запрос к API - Список ближайших станций
"""
import emoji
from api.base_get_requests import get_request
from config import YANDEX_API_KEY
from typing import Dict, Optional
from loguru import logger

TRANSPORT_VALUES = {
    "plane": "самолет",
    "train": "поезд",
    "suburban": "электричка",
    "bus": "автобус",
    "water": "водный транспорт",
    "helicopter": "вертолет",
}


async def request(
    lat: float, lng: float, station_type: str, distance: int
) -> Optional[str]:
    """
    Функция создает параметры для GET запроса, API Список ближайших станций(словарь), из полученных аргументов.
    Вызывает функцию get_request, модуля base_get_requests и передает в качестве аргументов переменные:
    params(словарь) и url. Переменная url - это адрес GET-запроса к API Яндекс Расписаний.

    Если результат функции get_request - None, возвращает None

    Если результат функции get_request - not None, возвращает результат работы функции forming_response,
    с передачей ей в качестве аргумента результат функции get_request.
    Args:
        distance: Передает радиус поиска
        station_type: Передает тип станции
        lng: Передает координаты долготы
        lat: Передает координаты широты

    Returns: forming_response or None
    """
    url = "https://api.rasp.yandex.net/v3.0/nearest_stations/"
    params = dict(
        apikey=YANDEX_API_KEY,
        lat=lat,
        lng=lng,
        station_types=station_type,
        distance=distance,
        limit=30,
    )

    result = await get_request(url=url, params=params)

    if result:
        return forming_response(data=result)
    return None


def forming_response(data: Dict) -> Optional[str]:
    """
    Функция извлекает и структурирует информацию. Принимает аргумент - словарь.
    В словаре данные полученные из GET запроса к API Яндекс Расписаний, раздел - Список ближайших станций.
    Возвращает строку структурированных данных, или None если отсутствуют ключи в словаре.

    Args:
        data: Передает данные, полученные из GET запроса.

    Returns: result
    Raises:
        Exception: При ошибке работе цикла

    """
    result = None

    try:
        if data.get("stations"):
            result = f'Найденная информация{emoji.emojize(":information:")}'

            for value in data.get("stations"):
                if value.get("station_type_name"):
                    result += "\nТип и название станции:\n{type} ".format(
                        type=value.get("station_type_name")
                    )

                if value.get("title"):
                    result += "- {name}\n".format(name=value.get("title"))

                if value.get("transport_type"):
                    result += "Тип транспорта: {type}\n".format(
                        type=TRANSPORT_VALUES.get(value.get("transport_type"))
                    )
                if value.get("distance"):
                    result += "Расстояние от вас: {km} км.\n".format(
                        km=int(value.get("distance"))
                    )

        logger.success("get_list_nearest_station > func forming_response")
        return result

    except Exception as err:
        logger.exception(err)
        return None
