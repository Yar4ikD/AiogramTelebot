from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboard.response_history import Buttons
from database.user_request_history.work_with_db import History
from loguru import logger


class Command(StatesGroup):

    __result = State()

    info_start = 'Укажите какое количество записей, мне нужно вывести в результате'

    @classmethod
    async def start(cls, message: types.Message, state: FSMContext) -> None:

        logger.info(f'User id: {message.from_user.id} | command: {message.text}')
        await cls.__result.set()
        await message.answer(text=cls.info_start, reply_markup=Buttons.how_many())

    @classmethod
    async def result(cls, message: types.Message, state: FSMContext) -> None:

        if message.text.isnumeric() or message.text in Buttons.count:

            response = History.select_data(user_id=str(message.from_user.id), count=message.text)
            if response:
                logger.success('Command | result')

                if len(response) > 4096:

                    for count in range(0, len(response), 4096):
                        await message.answer(text=response[count: count + 4095])
                else:
                    await message.answer(text=response)
                    await state.finish()

            else:
                logger.error(f'Result {response}')

                not_result = 'По Вашему запросу нет информации.'
                await message.answer(text=not_result)

    @classmethod
    async def register_command(cls, dp: Dispatcher) -> None:

        dp.register_message_handler(callback=cls.start, commands='history', state=None)
        dp.register_message_handler(callback=cls.result, state=cls.__result)
