import sys
import os
import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from loader import dp

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, '../keyboard', '../loader.py'))

from keyboard.basic_commands import list_command
# from loader import dp


async def information_bot(message: types.Message) -> None:
    """
    Функция запускает работу бота. Это первая функция при старте работы ТГ бота.
    Выводи пользователю, информацию - приветствие и список системных команд ТГ бота, в чат.
    Args:
        message: Передает сообщение от пользователя.

    Returns: None
    """
    emo_1 = emoji.emojize(':wave:', language='alias')
    emo_2 = emoji.emojize(':arrow_heading_down:', language='alias')
    info = f'<b>{message.chat.first_name} Привет.</b> {emo_1}\nЯ - Яндекс Бот Расписаний.\n' \
           f'\nЭто мои системные команды{emo_2}' \
           f'\n/help - выводит список моих команд.\nС этой команды тебе и нужно начать.\n' \
           f'\n/history — вывод истории запросов пользователей'

    await message.answer(text=info)
    await message.delete()


async def start_command(message: types.Message) -> None:
    """
    Функция выводи пользователю, список основных команд ТГ бота.
    Args:
        message: Передает чат - сообщение от пользователя.

    Returns: None
    """
    info = 'Список моих команд.\nВыбери идин из вариантов и нажми на кнопку.'

    await message.answer(text=info, reply_markup=list_command())
    await message.delete()


async def register_command_start(dp: Dispatcher) -> None:
    """
    Функция запускает регистрацию обработчиков сообщений, декораторов.
    Args:
        dp: Передает класс Dispather, библиотеке aiogram
    Returns: None
    """
    dp.register_message_handler(information_bot, Text(equals=['start', 'старт', '/start'], ignore_case=True))
    dp. register_message_handler(callback=start_command, commands=['help'])
