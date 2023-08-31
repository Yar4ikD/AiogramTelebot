"""В этом модуле созданы базовые кнопки ТГ-бота."""

import emoji
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import types
from aiogram_calendar import DialogCalendar


class UniversalButtons:
    """
    Базовый класс, в котором прописаны часто используемые кнопки ТГ-бота.
    """

    but_command_1 = KeyboardButton(
        text=f'Расписание рейсов между городами {emoji.emojize(":cityscape:")}'
    )
    but_command_2 = KeyboardButton(
        text=f'Расписание рейсов по станции {emoji.emojize(":bookmark_tabs:")}'
    )
    but_command_3 = KeyboardButton(
        text=f'Список ближайших станций {emoji.emojize(":trolleybus:")}'
    )

    but_continue = KeyboardButton(
        text=f'Продолжить {emoji.emojize(":fast-forward_button:")}'
    )
    but_step_back = KeyboardButton(
        text=f'{emoji.emojize(":fast_reverse_button:")} Вернуться назад'
    )
    but_command_again = KeyboardButton(
        text=f'Запусти команду заново {emoji.emojize(":repeat_button:")}'
    )
    but_list_command = KeyboardButton(
        text=f'Выведи список своих команд {emoji.emojize(":repeat_single_button:")}'
    )
    but_out = KeyboardButton(text=f'Выйти {emoji.emojize(":cross_mark_button:")}')

    @classmethod
    def list_command(cls) -> types.ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки и клавиатуру ТГ-бота.
        Применяется при старте бота или команды Помощь.
        Кнопки для вызова основных команд ТГ-бота.

        Returns: button_start

        """
        button_start = ReplyKeyboardMarkup(row_width=1)
        button_start.add(cls.but_command_1).add(cls.but_command_2).add(
            cls.but_command_3
        )
        return button_start

    @classmethod
    def calendar(cls) -> DialogCalendar:
        """
        Метод класса создает кнопки календаря, виджет календаря.
        Применяется при выборе даты.

        Returns: exm_calendar

        """
        exm_calendar = DialogCalendar()
        exm_calendar.months = [
            "Янв",
            "Февр",
            "Март",
            "Апр",
            "Май",
            "Июнь",
            "Июль",
            "Авг",
            "Сент",
            "Окт",
            "Ноя",
            "Дек",
        ]
        return exm_calendar
