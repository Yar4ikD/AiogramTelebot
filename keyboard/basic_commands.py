import emoji
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import types


def list_command() -> types.InlineKeyboardMarkup:
    """
    Функция создает экземпляры класса кнопки и клавиатуру.
    Кнопки это команды бота, его функции.
    Применяется при старте бота или команды Помощь.

    :return: button_start
    :type: InlineKeyboardMarkup

    """
    em_but = emoji.emojize(':memo:', language='alias')
    but_1 = InlineKeyboardButton(text=f'Расписание рейсов по станции {em_but}', callback_data='station_timetable')
    but_2 = InlineKeyboardButton(text='Список ближайших станций', callback_data='nearest_list')
    but_3 = InlineKeyboardButton(text='Список станций следования', callback_data='station_timetable')
    but_4 = InlineKeyboardButton(text='Список ближайших станций', callback_data='station_timetable')

    button_start = InlineKeyboardMarkup(row_width=1)
    button_start.add(but_1).add(but_2).add(but_3).add(but_4)

    # but_4 = KeyboardButton(text='Информация о перевозчике')
    # but_3 = KeyboardButton(text='Список станций следования')
    # but_2 = KeyboardButton(text='Список ближайших станций')

    # but_5 = KeyboardButton('Меню')

    # button_start = ReplyKeyboardMarkup(
    #     resize_keyboard=True,
    #     input_field_placeholder='Выбери один из вариантов:',
    #     one_time_keyboard=True
    # )
    # button_start.add(but_1).add(but_2).add(but_3).add(but_4)
    return button_start