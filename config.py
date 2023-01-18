import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')

ALL_COUNTRIES_CODE_JSON_PATH = os.path.realpath('../database/all_countries_code.json')
