import os
import sys
import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from keyboard.station_timetable_buttons import tru_or_false, show_list, output
from api.get_schedule_station import get_list_of_flights_with_description

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, '../database', '../loader.py'))

from database.CRUD_db import YandexDB
from loader import dp, bot


"""Модуль работы команды ТГ-бота - Расписание рейсов по станции."""


class QuestionsFSM(StatesGroup):
    """
    Класс наследует от базового класса StatesGrop.
    Создаем FSM состояние ТГ-бота.
    Атрибуты класса, являются флагами для запуска работы функций.
    Записывать полученную информацию от пользователя.

    Attributes:
        region: Экземпляр класса. Состояние бота при получении от пользователя название региона.
        settlement: Экземпляр класса. Состояние бота при получении от пользователя название города.
    """
    region = State()
    settlement = State()
    station = State()


async def get_start(callback: types.CallbackQuery, state: QuestionsFSM) -> None:
    """
    Функция запускает машинное состояние бота - FSM.
    Выводит пользователю, ответ в чат телеграмма, информацию
    (инструкцию о дальнейшем взаимодействии, пользователя с телеграм ботом).

    Args:
        callback: Передает обьект - входящий запрос обратного вызова с кнопки
        (Данные, связанные с кнопкой обратного вызова).
        state: Передает класс FSM состояния бота.

    Variables:
        info(str): Инструкция о дальнейшем взаимодействии, пользователя с телеграм ботом

    Returns: None
    """
    info = '<b>Укажи названия области.</b>\nНужно указать только название!\n' \
           '<b>Не добавляйте</b> какую либо приставку: (обл, рег. и т.д).\n' \
           'Пример:\n\t<b>Ярославская</b>\n\t<b>Московская</b>\n\t<b>Псковская</b>'

    await QuestionsFSM.region.set()
    await callback.message.answer(text=info, reply_markup=output())


async def get_region(message: types.Message, state: FSMContext):
    print(message)

    if message.text == 'Продолжить!':

        info = 'Введите название населенного пункта\n<b>Это обязательный параметр!</b>'

        await QuestionsFSM.next()
        await message.answer(text=info, reply_markup=output())
        await message.delete()

    else:

        answer = message.text.capitalize().strip()
        response = await YandexDB.select_region_or_settlement(user_msg=answer, type_query='region')

        if response:
            info = f'Вот что я нашел:\n<b>{response[1]}\n</b>\nЕсли это правильное названия, ' \
                   f'тогда нажмите - Продолжить!\nВ противном случае введите название области заново!'

            await message.reply(text=info, reply_markup=tru_or_false())
            await message.delete()

            async with state.proxy() as data:
                data['reg'] = response

        else:
            msg_error = 'Я не нашел в базе такой области.\nВведите название еще раз!'
            await message.reply(text=msg_error, reply_markup=output())
            await message.delete()


async def get_settlement(message: types.Message, state: FSMContext):

    if message.text == 'Продолжить!':
        info = 'Введите название станции или остановки.\n<b>Это обязательный параметр!</b>'

        await QuestionsFSM.next()
        await message.answer(text=info, reply_markup=show_list())
        await message.delete()

    else:

        answer = message.text.capitalize().strip()
        response = await YandexDB.select_region_or_settlement(user_msg=answer, type_query='settlement')

        if response:
            async with state.proxy() as data:
                data['city'] = response

            info = f'Вот что я нашел:\n<b>{response[1]}\n</b>\nЕсли это правильное названия, ' \
                   f'тогда нажмите - Продолжить!\nВ противном случае введите название населенного пункта заново!'

            await message.reply(text=info, reply_markup=tru_or_false())
            await message.delete()

        else:
            msg_error = 'Я не нашел в базе такого населенного пункта.\nВведите еще раз!'
            await message.reply(text=msg_error, reply_markup=output())
            await message.delete()


async def get_station(message: types.Message, state: FSMContext):

    if message.text == 'Показать список станций.':
        async with state.proxy() as data:
            response = await YandexDB.select_list_station(region_code=data['reg'][0], settlement_code=data['city'][0])

        if len(response):
            answer = 'Список станций и остановок:'
            for i, s, d in response:
                tmp = '\n<b>Название станции</b>:\n{name_st}\n<b>Тип</b>: {type}\n' \
                      '<b>Виды транспорта</b>: {transport}\n'.format(name_st=i, type=s, transport=d)
                answer += tmp

            await message.answer(text=answer)
            # await message.delete()

        else:
            info = 'К сожалению в этом населенном пункте, нет станций!'
            await message.reply(text=info, reply_markup=output())

    if message.text == 'Продолжить!':
        async with state.proxy() as data:
            result = await get_list_of_flights_with_description(station=data['stat'][0])
        await message.answer(result)
        await state.finish()

    elif message.text not in ['Продолжить!', 'Показать список станций.']:
        answer = message.text.capitalize().strip()
        async with state.proxy() as data:
            response = await YandexDB.select_yandex_code(user_msg=answer,
                                                         region=data['reg'][0], settlement=data['city'][0])

        if response:
            async with state.proxy() as data:
                data['stat'] = response

            info = f'Вот что я нашел:\n<b>{response}\n</b>\nЕсли это правильное название, ' \
                   f'тогда нажмите - Продолжить!\nВ противном случае введите название станции!'

            await message.reply(text=info, reply_markup=tru_or_false())
            await message.delete()

        else:
            msg_error = 'Я не нашел в базе такой станции.\nВведите еще раз!'
            await message.reply(text=msg_error, reply_markup=show_list())


async def stop_working(callback: types.CallbackQuery, state: FSMContext):
    now_state = await state.get_state()

    if now_state is None:
        return

    await state.finish()
    # await callback.message.reply(reply_markup=list_command())
    em_but = emoji.emojize(':memo:', language='alias')
    info = f'{callback.message.chat.first_name} вы вышли из раздела:\nРасписание рейсов по станции {em_but}'
    await callback.answer(text=info, show_alert=True)


async def register_command_timetable(dp: Dispatcher):

    dp.register_callback_query_handler(stop_working, text='out', state='*')
    dp.register_callback_query_handler(get_start, text='station_timetable', state=None)
    dp.register_message_handler(get_region, state=QuestionsFSM.region)
    dp.register_message_handler(get_settlement, state=QuestionsFSM.settlement)
    dp.register_message_handler(get_station, state=QuestionsFSM.station)

