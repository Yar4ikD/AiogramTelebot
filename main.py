from aiogram import executor
from loader import dp
from commands import start, station_timetable, list_nearest_stations
from database.CRUD_db import YandexDB


async def on_start(_) -> None:
    """ Функция, выводит на экран консоли сообщения, что бот работает.
        Установляивет соединения с БД.
        Запускает функции, для регистрации обработчиков команд ТГ-бота
    """
    print('Бот начал работать')
    await YandexDB.connect_db()
    await start.register_command_start(dp)
    await station_timetable.register_command_timetable(dp)
    await list_nearest_stations.register_command_nearest_station(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
