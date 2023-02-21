"""
    Модуль работы GET - запроса.
    Производиться запрос, обрабатывается ответ и возвращает результат.
    Функция модуля является базовой, для работы со всеми запросами к API Яндекс Расписаний и его разделов.
"""
import json
import requests
from loguru import logger
from typing import Dict, Optional


def get_request(url: str, params: Dict) -> Optional[Dict]:
    """
    Функция для работы с GET-запросами к API Яндекс Расписаний и его разделов.

    Args:
        url: Передает url адрес GET-запроса.
        params: Передает параметры запроса.

    Returns: json.loads(request.txt) or None
    Raises:
        RequestException: Если статус - код ответа, не равен 200.

    """
    try:
        request = requests.get(url=url, params=params)

        if request.status_code != 200:
            raise requests.RequestException(f'Статус ответа > {request.text}')

        logger.success('GET-запрос')
        return json.loads(request.text)

    except requests.RequestException as err:
        logger.exception(err)
        return None
