from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types


def start() -> types.ReplyKeyboardMarkup:
    """
    Функция создает экземпляры класса кнопки и клавиатуру.
    Кнопки это команды бота, его функции.
    Применяется при старте бота или команды Помощь.

    :return: button_start
    :type: ReplyKeyboardMarkup

    """

    but_4 = KeyboardButton('Информация о перевозчике')
    but_3 = KeyboardButton('Список станций следования')
    but_2 = KeyboardButton('Список ближайших станций')
    but_1 = KeyboardButton('Расписание рейсов по станции')
    # but_5 = KeyboardButton('/Команды')

    button_start = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder='Выбери один из вариантов:',
        one_time_keyboard=True
    )
    button_start.add(but_1).add(but_2).add(but_3).add(but_4)

    return button_start


