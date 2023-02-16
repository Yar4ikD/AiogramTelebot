from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboard.base import UniversalButtons


class Buttons(UniversalButtons):
    count = ('2', '5', '7', '10')

    @classmethod
    def how_many(cls) -> ReplyKeyboardMarkup:
        """
        Метод класса создает кнопки и клавиатуру ТГ-бота.
        Кнопки для передачи пользователем количества вывода результата команды.

        Returns: buttons

        """
        but = (KeyboardButton(text=text) for text in cls.count)
        buttons = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*but)
        return buttons
