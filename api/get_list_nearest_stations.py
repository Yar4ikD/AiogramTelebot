import asyncio
import json
import requests
from config import YANDEX_API_KEY, TRANSPORT_VALUES
from typing import Dict


async def get_nearest_stations(lat: float, lng: float, station_type: str, distance: int):

    try:
        request = requests.get(f'https://api.rasp.yandex.net/v3.0/nearest_stations/?apikey={YANDEX_API_KEY}'
                               f'&format=json'
                               f'&lat={lat}'
                               f'&lng={lng}'
                               f'&station_types={station_type}'
                               f'&distance={distance}'
                               f'&lang=ru_RU'
                               f'&limit=50'
                               )

        if request.status_code != 200:
            raise requests.RequestException(f'Статус код > {request.status_code}')

    except requests.RequestException as err:
        print(f'Ошибка ответа сервера!\n{err}')
        return 'Упс... что то пошло не так, при запросе к серверу.'

    else:
        data = json.loads(request.text)
        return await forming_response(data)


async def forming_response(data: Dict, limit: int = 30) -> str | None:

    count = 0
    try:
        if data.get('stations', None):
            result = '<b>По вашему запросу было найдено:</b>\n'

            for value in data.get('stations'):
                if count >= limit:
                    break
                station_type_name = '<b>Тип и название станции:</b>\n{type} - {name}'.format(
                    type=value.get('station_type_name'), name=value.get('title'))

                transport_type = '<b>Тип транспорта:</b> {type}'.format(
                    type=TRANSPORT_VALUES.get(value.get('transport_type'), '-'))

                distance = '<b>Расстояние от вас:</b> {km}км.'.format(km=int(value.get('distance')))

                # touch_url = '<b>Url Яндекс Расписание рейсов:</b>\n{url}'.format(
                #     url=value.get('type_choices').get('tablo').get('touch_url'))

                result += '\n'.join((station_type_name, transport_type, distance, '\n'))
                count += 1
            return result

        return None

    except Exception as err:
        print(f'Ошибка!\n{err}')
        return 'Упс... что то пошло не так, при запросе к серверу.'

# if __name__ == '__main__':
#     asyncio.run(get_nearest_stations())

