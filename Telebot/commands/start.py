from aiogram import types, Dispatcher
# from ..loader import dp


async def information_bot(message: types.Message):

    info = """
    Привет я Бот - Яндекс Расписаний.
    Что я могу найти для тебя:
    - <b>Расписание рейсов по станции</b>
    -
    -
    -

    """

    await message.answer(info)
    await message.delete()


def register_command_start(dp: Dispatcher):

    dp.register_message_handler(information_bot, commands=['hello-world', 'Привет'])
