"""
    Модуль работы команд ТГ-бота таких, как:
    Старт работы бота
    Список команд
    Выход из любой команды бота.
"""

import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboard.base import UniversalButtons
from database.user_request_history.work_with_db import History


async def information_bot(message: types.Message) -> None:
    """
    Функция запускает работу бота. Это первая функция при старте работы ТГ бота.
    Выводит пользователю, информацию - приветствие и список системных команд ТГ бота, в чат.

    Args:
        message: Передает сообщение от пользователя.

    Returns: None

    """
    History.add_user(
        user_id=message.from_user.id, user_name=message.from_user.first_name
    )

    emo_1 = emoji.emojize(":wave:", language="alias")
    emo_2 = emoji.emojize(":arrow_heading_down:", language="alias")
    info = (
        f"<b>{message.chat.first_name} Привет.</b> {emo_1}\nЯ - Яндекс Бот Расписаний.\n"
        f"Это мои системные команды{emo_2}\n"
        f"\n/help - выводит список моих команд.\nС этой команды тебе и нужно начать.\n"
        f"\n/history — вывод истории запросов пользователей"
    )

    await message.answer(text=info)
    await message.delete()


async def base_list_command(message: types.Message) -> None:
    """
    Функция-обработчик, выводит пользователю, список основных команд ТГ бота.
    Список представлен в виде KeyboardButton кнопок.

    Args:
        message: Передает чат - сообщение от пользователя.

    Returns: None

    """
    info = f'<b>Список моих команд.</b>{emoji.emojize(":down_arrow:")}'

    await message.answer(text=info, reply_markup=UniversalButtons.list_command())


async def base_stop_working(callback: types.Message, state: FSMContext) -> None:
    """
    Функция-обработчик, останавливает FSM состояния команд ТГ-бота.
    Выходит из команды(FSM состояния) и сообщает пользователю об удачному выходе из раздела.

    Args:
        callback: Передает объект - входящий запрос обратного вызова с кнопки
        state: Передает экземпляр класса State, FSM состояния бота.

    Returns: None

    """
    now_state = await state.get_state()
    if now_state is None:
        return

    await state.finish()
    em_but = emoji.emojize(":OK_hand:")
    info = f"{callback.chat.first_name} вы успешно вышли из раздела {em_but}"

    await callback.answer(text=info, reply_markup=UniversalButtons.list_command())


async def register_command(dp: Dispatcher) -> None:
    """
    Функция запускает регистрацию обработчиков сообщений, декораторов.

    Args:
        dp: Передает класс Dispatcher, библиотеке aiogram

    Returns: None

    """
    dp.register_message_handler(
        callback=base_stop_working, commands=UniversalButtons.but_out.text, state="*"
    )
    dp.register_message_handler(
        information_bot, Text(equals=["start", "старт", "/start"], ignore_case=True)
    )
    dp.register_message_handler(
        base_list_command,
        Text(equals=["/help", UniversalButtons.but_list_command.text]),
    )
