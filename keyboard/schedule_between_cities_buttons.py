"""Модуль отвечает за создание клавиатуры и кнопок ТГ-бота, команды Расписание рейсов между городами."""

import emoji
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from .base import UniversalButtons


class Buttons(UniversalButtons):
    """
        Класс наследует от базового класса UniversalButtons.
        Класс отвечает за создание кнопок и клавиатуры ТГ-Бота.
    """
    transport_type = ('Самолет', 'Поезд', 'Электричка', 'Автобус')

    @classmethod
    def tru_continue(cls) -> ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки ТГ-Бота. Кнопки: Продолжить, Вернуться назад, Выход из команды.
        Returns: buttons
        """
        buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(cls.but_continue).add(cls.but_step_back)
        return buttons

    @classmethod
    def back(cls) -> ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки ТГ-Бота. Кнопки: Вернуться назад.
        Returns: buttons
        """
        button = ReplyKeyboardMarkup(resize_keyboard=True).add(cls.but_step_back)
        return button

    @classmethod
    def transport(cls) -> ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки ТГ-Бота.
        Кнопки для выбора типа транспортного средства.
        Returns: buttons
        """
        but = (KeyboardButton(text=text) for text in cls.transport_type)
        buttons = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*but)
        return buttons

    @classmethod
    def menu_or_again(cls) -> ReplyKeyboardMarkup:
        buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(cls.but_command_again).add(cls.but_list_command)
        return buttons
