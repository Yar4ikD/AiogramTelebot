import os
from dotenv import load_dotenv, find_dotenv

"""Модуль содержит конфигурацию для запуска и работы ТГ-бота"""

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')

ALL_COUNTRIES_CODE_JSON_PATH = os.path.realpath('../database/create_database/all_countries_code.json')
DB_PATH = os.path.abspath('database/RusCode.db')
DB_HISTORY = os.path.abspath(os.path.join('database/history.db'))
