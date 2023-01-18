from python_basic_diploma.config import YANDEX_API_KEY
import requests
import json
import os

""" 
Модуль используется один раз.
Он запишет файл, который будет использоваться в сценарии для написания БД.
Его можно запустить как самостоятельный сценарий, строки функция main() и условия if.
"""


def get_code_create_file_json(path: str, api: str = YANDEX_API_KEY) -> None:
    """
    Функция делает АPI-запрос(GET) Список всех доступных станций - на сервис Яндекс Расписаний.
    Ответ содержит полный список станций, информацию о которых предоставляют Яндекс Расписания.

    Список структурирован географически:
        ответ содержит список стран со вложенными списками регионов и населенных пунктов,
        в которых находятся станции.
        Формат ответа JSON.

    При успешном ответе сервера, записывает ответ в файл формата - .json

    :param path: Путь к файлу для записи ответа.
    :param api: Ключ доступа к API
    :return: None or raise
    :raise TypeError: Если файл для записи не формата json
    :raise Exception: Если статус ответа запроса не равен 200
    """

    try:

        if not os.path.basename(path).endswith('.json'):
            raise TypeError(f'Файл {path} должен иметь расширение - .json')

        req = requests.get(f'https://api.rasp.yandex.net/v3.0/stations_list/?apikey={api}&lang=ru_Ru&format=json')

        if req.status_code != 200:
            raise Exception(f'Статус код запроса - {req.status_code}')

    except TypeError as err:
        print('Ошибка!', err, sep='\n')

    except Exception as err:
        print('Ошибка запроса к серверу Яндекс!', err, sep='\n')

    else:
        data = json.loads(req.text)
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


# def main():
#
#     get_code_create_file_json(YANDEX_API_KEY, 'file_test.json')
#
#
# if __name__ == '__main__':
#     main()