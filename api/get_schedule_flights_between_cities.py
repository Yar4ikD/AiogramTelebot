"""
    В данном модуле прописана логика работы,
    для получения списка рейсов, следующих от указанного населенного пункта отправления
    к указанному населенному пункту прибытия и информацию, по каждому рейсу от API Яндекс Расписаний,
    раздел Расписание рейсов между станциями
"""
import emoji
from config import YANDEX_API_KEY
from typing import Dict, Optional
from .base_get_requests import get_request
from loguru import logger


async def request(from_city: str, to_city: str, transport_type: str, date: str) -> Optional[str]:
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
        'apikey': YANDEX_API_KEY,
        'format': 'json',
        'from': from_city,
        'to': to_city,
        'transport_types': transport_type,
        'date': date,
        'limit': 10
    }

    url = 'https://api.rasp.yandex.net/v3.0/search/'

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
        if data.get('segments'):
            result = f'<b>Найденная информация</b>{emoji.emojize(":information:")}'
            for value in data.get('segments'):

                if value.get('from').get('title'):
                    result += '\nПункта отправления:\n{}\n'.format(value.get('from').get('title'))
                if value.get('departure_platform'):
                    result += 'Номер платформы станции отправления: {}\n'.format(value.get('departure_platform'))
                if value.get('departure_terminal'):
                    result += 'Терминал станции отправления: {}\n'.format(value.get('departure_terminal'))
                if value.get('departure'):
                    result += 'Время отправления:\n{}\n'.format(value.get('departure'))

                if value.get('to').get('title'):
                    result += 'Станция прибытия:\n{}\n'.format(value.get('to').get('title'))
                if value.get('arrival_platform'):
                    result += 'Номер платформы станции прибытия:\n{}\n'.format(value.get('arrival_platform'))
                if value.get('arrival_terminal'):
                    result += 'Терминал станции прибытия: {}\n'.format(value.get('arrival_terminal'))
                if value.get('arrival'):
                    result += 'Время прибытия:\n{}\n'.format(value.get('arrival'))

                if value.get('has_transfers'):
                    result += 'Наличия пересадок по ходу рейса!\n'
                if value.get('duration'):
                    result += 'Продолжительность рейса: {}\n'.format(value.get('duration'))
                if value.get('tickets_info'):
                    flag = 'Возможно.' if value.get('tickets_info').get('et_marker') else 'Нет'
                    result += 'Купить электронный билет: {}\n'.format(flag)

                result += '\nИнформация о нитке рейса\n'
                if value.get('thread').get('title'):
                    result += 'Название нитки:\n{}\n'.format(value.get('thread').get('title'))
                if value.get('thread').get('number'):
                    result += 'Номер рейса: {}\n'.format(value.get('thread').get('number'))
                if value.get('thread').get('vehicle'):
                    result += 'Название транспортного средства:\n{}\n'.format(value.get('thread').get('vehicle'))

                result += '\nИнформация о перевозчике.\n'
                if value.get('thread').get('carrier').get('title'):
                    result += 'Перевозчик: {}\n'.format(value.get('thread').get('carrier').get('title'))
                if value.get('thread').get('carrier').get('phone'):
                    result += 'Номер телефона:\n{}\n'.format(value.get('thread').get('carrier').get('phone'))
                if value.get('thread').get('carrier').get('url'):
                    result += 'Сайт перевозчика:\n{}\n'.format(value.get('thread').get('carrier').get('url'))
                result += '-' * 10

        return result

    except Exception as err:
        logger.exception(err)
        return None
