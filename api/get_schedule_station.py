"""
    Модуль для работы с GET-запросами.
    Запрос к API - Расписание рейсов по станции.
"""

import datetime
from loguru import logger
from config import YANDEX_API_KEY
from typing import Dict, Optional
from .base_get_requests import get_request


async def request(station_code: str, date=datetime.datetime.today(), transport: str = 'suburban',
                  event: str = 'arrival') -> Optional[str]:
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
        'apikey': YANDEX_API_KEY,
        'station': station_code,
        'format': 'json',
        'date': date,
        'transport_types': transport,
        'event': event,
        'direction': 'all',
        # 'result_timezone': 'Europe/Moscow'
    }
    url = 'https://api.rasp.yandex.net/v3.0/schedule/'
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
    try:
        result = ''
        if data.get('station').get('title'):
            result += '<b>Станция:</b>\n{data}\n'.format(data=data.get('station').get('title'))
        if data.get('station').get('station_type_name'):
            result += '<b>Тип станции:</b> {data}\n'.format(data=data.get('station').get('station_type_name'))
        if data.get('date'):
            result += '<b>Дата:</b> {date}\n'.format(date=data.get('date'))

        for count, value in enumerate(data.get('schedule')):
            if count >= limit:
                break

            if value.get('thread').get('title'):
                result += '\nНазвание нитки:\n{data}\n'.format(data=value.get('thread').get('title'))
            if value.get('thread').get('number'):
                result += 'Номер рейса: {data}\n'.format(data=value.get('thread').get('number'))

            if value.get('terminal'):
                result += 'Терминал аэропорта: {data}\n'.format(data=value.get('terminal'))
            if value.get('platform'):
                result += 'Платформа отправления рейса:\n{data}\n'.format(data=value.get('platform'))

            if value.get('departure'):
                result += 'Время отправления:\n{data}\n'.format(data=value.get('departure'))
            if value.get('arrival'):
                result += 'Время прибытия:\n{data}\n'.format(data=value.get('arrival'))
            if value.get('days'):
                result += 'Дни курсирования нитки: {data}\n'.format(data=value.get('days'))

            if value.get('thread').get('carrier').get('title'):
                result += 'Перевозчик:\n{data}\n'.format(data=value.get('thread').get('carrier').get('title'))
            if value.get('thread').get('vehicle'):
                result += 'Транспортное средство:\n{data}\n'.format(data=value.get('thread').get('vehicle'))
            if value.get('thread').get('transport_subtype').get('title'):
                result += '{data}\n'.format(data=value.get('thread').get('transport_subtype').get('title'))

        return result

    except Exception as err:
        logger.exception(err)
        return None
