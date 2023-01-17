import sys
import os
from aiogram import types, Dispatcher

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, '../keyboard', '../loader.py'))

from keyboard.client_buttons import start
from loader import dp


# @dp.message_handler(commands=['start', 'Команды'])
async def information_bot(message: types.Message):

    info = """ 
    <b>Привет.</b>\nЯ - Яндекс Бот Расписаний.
Вот чем я могу тебе помочь, мои команды:
    
    <b>Расписание рейсов по станции</b>
    <b>Список ближайших станций</b>
    <b>Список станций следования</b>
    <b>Информация о перевозчике</b>

    """

    await message.answer(info, reply_markup=start())
    await message.delete()


def register_command_start(dp: Dispatcher):

    dp.register_message_handler(information_bot, commands=['start', 'Команды'])

