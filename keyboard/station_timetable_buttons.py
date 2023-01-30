import emoji
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import types


def tru_or_false() -> types.ReplyKeyboardMarkup:

    but_1 = KeyboardButton('Продолжить!')
    # but_2 = KeyboardButton('Выйти')

    button = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder='Выбери один из вариантов:',
        one_time_keyboard=True
    )
    button.add(but_1)#.add(but_2)

    return button


def show_list() -> types.ReplyKeyboardMarkup:

    but_1 = KeyboardButton('Показать список станций.')
    # but_2 = KeyboardButton('Выйти')

    button = ReplyKeyboardMarkup(
        # resize_keyboard=True,
        # input_field_placeholder='Введите название или Выбери один из вариантов:',
        # one_time_keyboard=True
    )
    button.add(but_1)#.add(but_2)

    return button


def output() -> types.InlineKeyboardMarkup:

    but_1 = InlineKeyboardButton(f'Выйти {emoji.emojize(":stop_sign:")}', callback_data='out')

    button = InlineKeyboardMarkup(row_width=1)
        # resize_keyboard=True,
        # one_time_keyboard=True
    # )
    button.add(but_1)

    return button

