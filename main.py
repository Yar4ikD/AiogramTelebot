from aiogram import executor
from loader import dp
from commands import base_command, station_timetable, list_nearest_stations, schedule_flights_between_cities, response_history
from database.codes_db import YandexDB
from loguru import logger

logger.add(sink='logg.log', format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}",
           rotation="50 MB", retention="1 day", compression='zip', colorize=True)


async def on_start(_) -> None:
    """ Функция, выводит в консоль сообщения, что бот работает.
        Установляивет соединения с БД.
        Запускает функции, для регистрации обработчиков команд ТГ-бота
    """

    try:
        await YandexDB.connect_db()
        await base_command.register_command(dp)
        await response_history.Command.register_command(dp)
        await schedule_flights_between_cities.Command.register_command(dp)
        await station_timetable.Command.register_command(dp)
        await list_nearest_stations.Command.register_command(dp)
        logger.info('Bot start work')
    except Exception as err:
        logger.exception(err)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
