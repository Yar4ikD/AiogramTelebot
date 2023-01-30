import asyncio
import datetime
import json
import requests
from config import YANDEX_API_KEY
from typing import Dict


async def get_list_of_flights_with_description(station: str, direction: str = '', transport: str = 'suburban',
                                               event: str = 'arrival',
                                               date=datetime.datetime.today()
                                               ) -> str:

    print(f'work > api requests {station}')
    try:
        req = requests.get(f'https://api.rasp.yandex.net/v3.0/schedule/?'
                           f'apikey={YANDEX_API_KEY}'
                           f'&station={station}'
                           f'&transport_types={transport}'
                           # f'&direction={direction}'
                           f'&event={event}'
                           f'&date={date}'

                           )

        if req.status_code != 200:
            raise requests.RequestException(f'Статус код > {req.status_code}')

    except requests.RequestException as err:
        print(f'Ошибка ответа сервера!\n{err}')
        return 'Упс... что то пошло не так, при запросе к серверу.'

    else:
        data = json.loads(req.text)
        return await forming_response(data)


async def forming_response(data: Dict, limit: int = 10) -> str:
    result = ''
    count = 0
    try:
        date = '<b>Дата:</b> {date}'.format(date=data.get('date', 'Время не указанно.'))
        info_station = '<b>Название станции:</b>\n{data}'.format(data=data.get('station', {}).get('title', None))
        station_type_name = '<b>Тип станции:</b> {data}\n'.format(data=data.get('station', {}).get('station_type_name', None))
        result = '\n'.join((date, info_station, station_type_name))

        for value in data.get('schedule'):
            if count >= limit:
                break

            number = 'Номер рейса: {data}'.format(data=value.get('thread').get('number', 'Отсутствует.'))
            title = 'Название нитки:\n{data}'.format(data=value.get('thread').get('title', 'Отсутствует.'))
            carrier = 'Перевозчик:\n{data}'.format(data=value.get('thread').get('carrier').get('title', '-'))
            code = 'Код перевозчика: {data}'.format(data=value.get('thread').get('carrier').get('code', '-'))
            platform = 'Платформа или путь, с которого отправляется рейс:\n{data}'.format(data=value.get('platform', '-'))
            terminal = 'Терминал аэропорта:\n{data}'.format(data=value.get('terminal', '-'))
            days = 'Дни курсирования нитки\n{data}'.format(data=value.get('days', '-'))
            except_days = 'Дни, в которые нитка не курсирует\n{data}'.format(data=value.get('except_days', '-'))
            departure = 'Время отправления:\n{data}'.format(data=value.get('departure', '-'))
            arrival = 'Время прибытия:\n{data}'.format(data=value.get('arrival', '-'))

            result += '\n'.join((number, title, carrier, code, platform, terminal, days, except_days, departure, arrival))
            count += 1
        return result

    except Exception as err:
        print(f'Ошибка!\n{err}')
        result = 'Упс... что то пошло не так, при запросе к серверу.'

    finally:
        return result
