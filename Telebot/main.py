from aiogram import executor
from loader import dp
from commands import start


async def on_start(_) -> None:
    """ Служебная функция, выводит на экран консоли сообщения, что бот работает. """
    print('Бот начал работать')


start.register_command_start(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
