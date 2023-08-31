"""
    Модуль работы команды ТГ-бота: История запросов пользователя.
"""

import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from commands.base_command import base_stop_working
from keyboard.response_history import Buttons
from database.user_request_history.work_with_db import History
from loguru import logger


class Command(StatesGroup):
    """
    Подкласс наследует от базового класса StatesGroup.
    В классе прописана работа команды ТГ-бота: История запросов пользователя.
    Приватные атрибуты класса это FSM состояние ТГ-бота.
    """

    __result = State()

    info_start = (
        f"Укажите какое количество записей нужно вывести в результате"
        f'{emoji.emojize(":backhand_index_pointing_down:")}'
    )

    not_result = "Я не нашел ваш id в базе данных. Ваша история запросов пустая."

    @classmethod
    async def start(cls, message: types.Message, state: FSMContext) -> None:
        logger.info(f"User id: {message.from_user.id} | command: {message.text}")
        await cls.__result.set()
        await message.answer(text=cls.info_start, reply_markup=Buttons.how_many())

    @classmethod
    async def result(cls, message: types.Message, state: FSMContext) -> None:
        if message.text.isnumeric() or message.text in Buttons.count:
            response = History.select_data(
                user_id=str(message.from_user.id), count=message.text
            )
            if response:
                logger.success("Command | result")

                if len(response) > 4096:
                    for count in range(0, len(response), 4096):
                        await message.answer(text=response[count: count + 4095])
                else:
                    await message.answer(text=response)
                    await state.finish()

            else:
                logger.error(f"Result {response}")
                await message.answer(text=cls.not_result)

    @classmethod
    async def register_command(cls, dp: Dispatcher) -> None:
        dp.register_message_handler(callback=cls.start, commands="history", state=None)
        dp.register_message_handler(
            base_stop_working, Text(Buttons.but_out.text), state="*"
        )
        dp.register_message_handler(callback=cls.result, state=cls.__result)
