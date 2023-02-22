"""
    Модуль работы с клавиатурой и кнопками ТГ-бот
    В этом модуле находятся функции которые, создают и регистрируют кнопки ТГ-бота
    Функции модуля используются в работе скрипта - list_nearest_stations.
"""

import emoji
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from .base import UniversalButtons


class Buttons(UniversalButtons):

    buttons_distance = ('5', '10', '20', '30', '40', '50')

    but_stations_type = {
        'Автовокзал': 'bus_station',
        'Аэропорт': 'airport',
        'Aвтобусная остановка': 'bus_stop',
        'Вокзал': 'train_station'
    }

    @classmethod
    def location(cls) -> ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки и клавиатуру ТГ-бота.
        Кнопка для передачи пользователем соей геолокации.

        Returns: buttons

        """
        but = KeyboardButton(text=f'Поделиться геолокацией {emoji.emojize(":globe_showing_Asia-Australia:")}',
                             request_location=True)
        buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(but).add(cls.but_out)
        return buttons

    @classmethod
    def stations_type(cls) -> ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки и клавиатуру ТГ-бота.
        Кнопки для передачи пользователем типа станции.

        Returns: buttons

        """
        but = (KeyboardButton(text=text) for text in cls.but_stations_type)
        buttons = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*but)
        buttons.add(cls.but_step_back).add(cls.but_out)
        return buttons

    @classmethod
    def distance(cls) -> ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки и клавиатуру ТГ-бота.
        Кнопки для передачи пользователем радиуса поиска станции.

        Returns: buttons

        """
        but = (KeyboardButton(text=text) for text in cls.buttons_distance)
        buttons = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(*but)
        buttons.add(cls.but_step_back).add(cls.but_out)
        return buttons

    @classmethod
    def tru_continue(cls) -> ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки и клавиатуру ТГ-бота.
        Кнопка подтверждение ввода данных пользователем, возвращение назад и выход из команды.

        Returns:

        """
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.add(cls.but_continue).add(cls.but_step_back).add(cls.but_out)
        return buttons

    @classmethod
    def result(cls) -> ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки и клавиатуру ТГ-бота.
        Кнопки Выход и вернуться назад.
        Используются при ошибке результата работы команды.

        Returns: buttons

        """
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.add(cls.but_step_back).add(cls.but_out)
        return buttons

    # @classmethod
    # def exit(cls) -> ReplyKeyboardMarkup:
    #     """
    #     Метод класса создает кнопки и клавиатуру ТГ-бота.
    #     Кнопка Вывести список команд.
    #     Используется при корректном завершении работы команды.
    #
    #     Returns: buttons
    #
    #     """
    #     buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(cls.but_list_command)
    #
    #     return buttons
