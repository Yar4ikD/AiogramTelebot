"""Модуль отвечает за создание клавиатуры и кнопок ТГ-бота, команды Расписание рейсов по станции."""

import emoji
from .base import UniversalButtons
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types


class Buttons(UniversalButtons):
    """
    Класс наследует от базового класса UniversalButtons.
    Класс отвечает за создание кнопок и клавиатуры ТГ-Бота.
    """

    event_and_transport = {
        "Cамолет/Прибытие": ("plane", "arrival"),
        "Cамолет/Отправление": ("plane", "departure"),
        "Поезд/Прибытие": ("train", "arrival"),
        "Поезд/Отправление": ("train", "departure"),
        "Электричка/Прибытие": ("suburban", "arrival"),
        "Электричка/Отправление": ("suburban", "departure"),
        "Автобус/Прибытие": ("bus", "arrival"),
        "Автобус/Отправление": ("bus", "departure"),
    }
    but_list_stations = KeyboardButton(
        f'Показать список станций{emoji.emojize(":card_file_box:")}'
    )

    @classmethod
    def event_transport(cls) -> types.ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки ТГ-Бота, тип транспортного средства, и направление.
        Returns: buttons

        """
        but = (KeyboardButton(text=text) for text in cls.event_and_transport)
        buttons = ReplyKeyboardMarkup(
            resize_keyboard=True, row_width=2, one_time_keyboard=False
        ).add(*but)
        buttons.add(cls.but_out)
        return buttons

    @classmethod
    def tru_continue(cls) -> types.ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки ТГ-Бота. Кнопки: Продолжить, Вернуться назад, Выход из команды.
        Returns: buttons
        """
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.add(cls.but_continue).add(cls.but_step_back).add(cls.but_out)
        return buttons

    @classmethod
    def show_list(cls) -> types.ReplyKeyboardMarkup:
        """
        Метод класса, создает кнопку ТГ-бота: Список станций населенного пункта
        Returns: button
        """
        button = ReplyKeyboardMarkup(resize_keyboard=True)
        button.add(cls.but_list_stations).add(cls.but_step_back).add(cls.but_out)
        return button

    @classmethod
    def output(cls) -> types.ReplyKeyboardMarkup:
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.add(cls.but_step_back).add(cls.but_out)

        return buttons
