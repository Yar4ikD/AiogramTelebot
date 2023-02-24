"""
    Модуль работы GET - запроса.
    Производиться запрос, обрабатывается ответ и возвращает результат.
    Функция модуля является базовой, для работы со всеми запросами к API Яндекс Расписаний и его разделов.
"""
import json
import aiohttp
from loguru import logger
from typing import Dict, Optional


async def get_request(url: str, params: Dict) -> Optional[Dict]:
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
        async with aiohttp.ClientSession() as req:
            async with req.get(url=url, params=params) as response:

                if response.status != 200:
                    raise Exception(f'Статус ответа > {response.text}')
                response = await response.text()

        logger.success('GET-запрос')
        return json.loads(response)

    except Exception as err:
        logger.exception(err)
        return None
