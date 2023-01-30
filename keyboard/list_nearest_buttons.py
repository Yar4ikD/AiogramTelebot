import emoji
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram import types

"""
    Модуль работы с клавиатурой и кнопками ТГ-бот
    В этом модуле находятся функции которые создают и регистрируют кнопки ТГ-бота
    Методы Модуля используются в работе скрипта - list_nearest_stations.
"""


def button_location() -> types.ReplyKeyboardMarkup:
    """
    Функция создает кнопки и клавиатуру ТГ-бота.
    Кнопка для передачи пользователем соей геолокации.
    Returns: buttons
    """
    but = KeyboardButton(text='Поделиться геолокацией', request_location=True)
    but_2 = InlineKeyboardButton(f'Выйти {emoji.emojize(":stop_sign:")}', callback_data='out')

    buttons = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    buttons.add(but).add(but_2)
    return buttons


def button_stations_type() -> types.InlineKeyboardMarkup:
    """
    Функция создает кнопки и клавиатуру ТГ-бота.
    Кнопки для передачи пользователем тип станции.
    Returns: buttons
    """
    but_1 = InlineKeyboardButton(text='Aвтобусная остановка', callback_data='bus_stop')
    but_2 = InlineKeyboardButton(text='Автовокзал', callback_data='bus_station')
    but_3 = InlineKeyboardButton(text='Вокзал', callback_data='train_station')
    but_4 = InlineKeyboardButton(text='Аэропорт', callback_data='airport')
    # but_5 = InlineKeyboardButton(text='Все выше перечисленное',
    #                              callback_data='bus_stop, bus_station, train_station, airport'
    #                              )
    but_6 = InlineKeyboardButton(f'Выйти {emoji.emojize(":stop_sign:")}', callback_data='out')

    buttons = InlineKeyboardMarkup(row_width=1)
    buttons.add(but_4, but_2, but_3, but_1).add(but_6)
    return buttons


def button_distance() -> InlineKeyboardMarkup:
    """
    Функция создает кнопки и клавиатуру ТГ-бота.
    Кнопки для передачи пользователем радиуса поиска станции.
    Returns: buttons
    """
    but_1 = InlineKeyboardButton(text='до 10 км.', callback_data='10')
    but_2 = InlineKeyboardButton(text='до 25 км.', callback_data='25')
    but_3 = InlineKeyboardButton(text='до 35 км.', callback_data='35')
    but_4 = InlineKeyboardButton(f'Выйти {emoji.emojize(":stop_sign:")}', callback_data='out')

    buttons = InlineKeyboardMarkup(row_width=3)
    buttons.add(but_1, but_2, but_3).add(but_4)
    return buttons


def add_distance() -> InlineKeyboardMarkup:
    """
    Функция создает кнопки и клавиатуру ТГ-бота.
    Кнопки для передачи пользователем радиуса поиска станции.
    Returns: buttons
    """
    but_5 = InlineKeyboardButton(text='до 25 км.', callback_data='25')
    but_4 = InlineKeyboardButton(text='до 35 км.', callback_data='35')
    but_3 = InlineKeyboardButton(text='до 55 км.', callback_data='10')
    but_2 = InlineKeyboardButton(text='до 75 км.', callback_data='25')
    but_1 = InlineKeyboardButton(text='до 85 км.', callback_data='35')

    buttons = InlineKeyboardMarkup(row_width=3)
    buttons.add(but_1, but_2, but_3, but_4, but_5)
    return buttons
