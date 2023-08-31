"""
    В этом модуле прописана логика работы команды ТГ-бота: Расписание рейсов между городами.
    Весь функционал команды ТГ-бота, прописан на основе класса.
"""
import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData
from aiogram.types import ReplyKeyboardRemove
from aiogram_calendar import dialog_cal_callback

from commands.base_command import base_stop_working
from database.select_data_for_command.for_schedule_flights_between_cities import Select
from database.user_request_history.work_with_db import History
from keyboard.schedule_between_cities_buttons import Buttons
from api.get_schedule_flights_between_cities import request
from loguru import logger


class Command(StatesGroup):
    """
    Подкласс наследует от базового класса StatesGroup.
    В классе прописана работа команды ТГ-бота: Расписание рейсов между городами.
    Приватные атрибуты класса это FSM состояние ТГ-бота.
    """

    __transport_type = State()
    __form_region = State()
    __from_city = State()
    __to_region = State()
    __to_city = State()
    __date = State()
    __finish = State()

    info_start = (
        f"Для получения расписаний рейсов между городами, вам нужно будет поэтапно указать:\n"
        f"\n1. Тип транспорта\n2. Регион и город отправления\n3. Регион и город прибытия\n4. Дату.\n"
        f'\nСейчас, укажите - Тип транспорта{emoji.emojize(":backhand_index_pointing_down:")}'
    )
    info_from_city = (
        f'Укажите город отправления {emoji.emojize(":backhand_index_pointing_down:")}'
    )
    info_from_region = (
        f'Укажите регион отправления {emoji.emojize(":backhand_index_pointing_down:")}'
    )
    info_to_city = (
        f'Укажите город прибытия {emoji.emojize(":backhand_index_pointing_down:")}'
    )
    info_to_region = (
        f'Укажите регион прибытия {emoji.emojize(":backhand_index_pointing_down:")}'
    )
    info_transport_type = "Укажите тип транспортного средства"
    info_get_date = f'Укажите дату {emoji.emojize(":calendar:")} на которую необходимо получить список рейсов'
    info_not_result = "К сожалению, по вашему запросу нет информации!"

    msg_error_region = (
        f'{emoji.emojize(":person_shrugging:")} Я не нашел в базе такой области.'
        f"\nУкажите название еще раз!"
    )
    msg_error_city = (
        "Я не нашел в базе такого города.\nЭто может быть из-за 2х причин:"
        "\n1.Неверно указно название города.\n2.В городе нет <b>типа транспорта</b>, "
        "который вы указали ранее.\nУкажите название еще раз или измените тип транспорта!"
    )
    error_msg_no_sense = "Что это значить, я не понимаю Вас.\nВыберите одну из команд."

    data_keys = ("from_region", "from_city", "to_region", "to_city")
    transport_type_dict = {
        "Самолет": "plane",
        "Поезд": "train",
        "Электричка": "suburban",
        "Автобус": "bus",
    }

    @classmethod
    async def start_work(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса запускает процесс работы команды ТГ-бота.
        Запускает машинное состояние бота - FSM __transport_type.
        Выводит пользователю, инструкцию о дальнейшем взаимодействии, пользователя с командой ТГ-бота.

        Args:
            message: Передает сообщения
            state: Передает FSM состояние бота, None.

        Returns: None

        """
        logger.info(f"User id: {message.from_user.id} | command: {message.text}")
        await cls.__transport_type.set()
        await message.answer(text=cls.info_start, reply_markup=Buttons.transport())

    @classmethod
    @logger.catch()
    async def _universal(
        cls,
        message: types.Message,
        state: FSMContext,
        data_key: str = None,
        reg_code: str = None,
        msg_cont: str = None,
        msg_step_back: str = None,
        msg_error: str = None,
        markup_back=Buttons.back(),
        markup=ReplyKeyboardRemove(),
    ) -> None:
        """
        Метод класса для обработки сообщений от пользователя.
        Является универсальным обработчиком для 4х состояний бота:
        __form_region, __from_city, __to_region, __to_city.
        reg_code является флагом для запросов к БД.
        Args:
            message: Передает сообщение от пользователя
            state: Передает FSM состояние
            data_key: Передает ключ из кортежа data_keys
            reg_code: Передает код региона
            msg_cont: Передает сообщение, инструкцию для дальнейше работы с командой бота
            msg_step_back: Передает сообщение, инструкцию работы, предыдущим FSM состояния бота
            msg_error: Передает сообщение ошибки
            markup_back: Передает кнопки бота, предыдущего раздела
            markup: Передает кнопки бота.

        Returns: None

        """
        if (
            message.text == Buttons.but_continue.text
        ):  # подтверждение ввода данных, продолжение работы команды
            await cls.next()  # переключает на следующее FSM состояния.
            await message.answer(text=msg_cont, reply_markup=markup)
            await message.delete()

        elif (
            message.text == Buttons.but_step_back.text
        ):  # возвращаем бота в предыдущее FSM состояния
            await cls.previous()
            await message.reply(text=msg_step_back, reply_markup=markup_back)

        else:
            user_msg = message.text.capitalize().strip()
            if reg_code:
                response = await Select.settle(user_msg=user_msg, region_code=reg_code)
            else:
                response = await Select.region(user_msg=user_msg)

            if response and len(response[1]) > 1:
                info = (
                    f"Вот что я нашел:\n<b>{response[1]}\n</b>Если все правильно, нажмите "
                    f"<b>{Buttons.but_continue.text}</b>\nВ противном случае укажите название заново!"
                )

                logger.info(f"User data: {response[1]}")
                await message.reply(text=info, reply_markup=Buttons.true_continue())
                async with state.proxy() as data:
                    data[data_key] = response[0]

            else:
                await message.reply(text=msg_error, reply_markup=Buttons.back())

    @classmethod
    async def get_transport_type(
        cls, message: types.Message, state: FSMContext
    ) -> None:
        """
        Метод класса обрабатывает данные о Типе транспорта.
        Переключает FSM состояние на __form_region.
        Args:
            message: Передает сообщение от пользователя
            state: Передает FSM состояние бота, __transport_type

        Returns: None

        """
        if message.text in Buttons.transport_type:
            logger.info(f"Enter transport type > {message.text}")

            async with state.proxy() as data:
                data["transport_type"] = cls.transport_type_dict.get(message.text)
            await cls.next()
            await message.answer(
                text=cls.info_from_region, reply_markup=ReplyKeyboardRemove()
            )

        else:
            await message.reply(
                text="Что это за транспорт?\nВыбери из моего списка",
                reply_markup=Buttons.transport(),
            )

    @classmethod
    async def get_from_region(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса обрабатывает данные от пользователя, название региона отправления.
        Делает запрос к БД, для получения кода региона, указанного пользователем.
        Переключает FSM состояние на __from_city.
        Вызывает универсальный метод и передает в качестве аргументов, данные полученные от пользователя.
        Args:
            message: Передает название региона отправления
            state: Передает FSM состояние бота, __form_region.

        Returns: None

        """
        data_key = cls.data_keys[0]
        await cls._universal(
            message=message,
            state=state,
            data_key=data_key,
            msg_cont=cls.info_from_city,
            msg_step_back=cls.info_start,
            msg_error=cls.msg_error_region,
            markup_back=Buttons.transport(),
        )

    @classmethod
    async def get_from_city(
        cls, message: [types.Message, types.CallbackQuery], state: FSMContext
    ) -> None:
        """
        Метод класса обрабатывает данные от пользователя, название населенного пункта отправления.
        Делает запрос к БД, для получения кода населенного пункта, указанного пользователем.
        Переключает FSM состояние на __to_region.
        Вызывает универсальный метод и передает в качестве аргументов, данные полученные от пользователя.
        Args:
            message: Передает название населенного пункта отправления
            state: Передает FSM состояние бота, __from_city.

        Returns: None

        """
        data_key = cls.data_keys[1]
        async with state.proxy() as data:
            reg_code = data.get(cls.data_keys[0])

        await cls._universal(
            message=message,
            state=state,
            data_key=data_key,
            reg_code=reg_code,
            msg_cont=cls.info_to_region,
            msg_step_back=cls.info_from_region,
            msg_error=cls.msg_error_city,
        )

    @classmethod
    async def get_to_region(
        cls, message: [types.Message, types.CallbackQuery], state: FSMContext
    ):
        """
        Метод класса обрабатывает данные от пользователя, название региона прибытия.
        Делает запрос к БД, для получения кода региона, указанного пользователем.
        Переключает FSM состояние на __to_city.
        Вызывает универсальный метод и передает в качестве аргументов, данные полученные от пользователя.
        Args:
            message: Передает название региона прибытия
            state: Передает FSM состояние бота, __to_region.

        Returns: None

        """
        data_key = cls.data_keys[2]
        await cls._universal(
            message=message,
            state=state,
            data_key=data_key,
            msg_cont=cls.info_to_city,
            msg_step_back=cls.info_from_city,
            msg_error=cls.msg_error_region,
        )

    @classmethod
    async def get_to_city(cls, message: types.Message, state: FSMContext):
        """
        Метод класса обрабатывает данные от пользователя, название населенного пункта прибытия.
        Делает запрос к БД, для получения кода населенного пункта, указанного пользователем.
        Переключает FSM состояние на __date.
        Вызывает универсальный метод и передает в качестве аргументов, данные полученные от пользователя.
        Args:
            message: Передает название населенного пункта прибытия
            state: Передает FSM состояние бота, __to_city.

        Returns: None

        """
        data_key = cls.data_keys[3]
        async with state.proxy() as data:
            reg_code = data.get(cls.data_keys[2])
        await cls._universal(
            message=message,
            state=state,
            data_key=data_key,
            reg_code=reg_code,
            msg_cont=cls.info_get_date,
            msg_error=cls.msg_error_city,
            msg_step_back=cls.info_to_region,
            markup=await Buttons.calendar().start_calendar(),
        )

    @classmethod
    async def get_calendar(
        cls,
        callback_query: types.CallbackQuery,
        callback_data: CallbackData,
        state: FSMContext,
    ):
        """
        Метод класса, обрабатывает данные виджета календаря.
        Переводит FSM бота в состояние __finish.

        Args:
            callback_query: Передает кнопки календаря
            callback_data: Передает данные кнопок календаря
            state: Передает FSM состояние бота, __date.

        Returns: None

        """
        if isinstance(callback_query, types.CallbackQuery):
            selected, date = await Buttons.calendar().process_selection(
                callback_query, callback_data
            )

            if selected:
                await callback_query.message.answer(
                    f'Указанная вами дата: <b>{date.strftime("%Y-%m-%d")}</b>',
                    reply_markup=Buttons.true_continue(),
                )

                logger.info(f'Enter date > {date.strftime("%Y-%m-%d")}')
                async with state.proxy() as data:
                    data["date"] = date.strftime("%Y-%m-%d")
                await cls.next()

    @classmethod
    async def result(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод обработчик, возвращает пользователю информацию запроса.
        Останавливает FSM состояние команды бота.
        Завершает работу команды ТГ-бота.

        Args:
            message: Передает сообщение от пользователя
            state: Передает FSM состояние бота, __finish.

        Returns: None

        """

        if (
            message.text == Buttons.but_step_back.text
        ):  # возвращаем бота в предыдущее FSM состояния
            await cls.previous()
            await message.answer(
                text=cls.info_get_date,
                reply_markup=await Buttons.calendar().start_calendar(),
            )

        elif message.text == Buttons.but_command_again.text:
            await cls.first()
            await message.reply(text=cls.info_start, reply_markup=Buttons.transport())

        elif message.text == Buttons.but_continue.text:
            async with state.proxy() as data:
                from_city, to_city = data.get(cls.data_keys[1]), data.get(
                    cls.data_keys[3]
                )
                transport, date = data.get("transport_type"), data.get("date")
                query_data = f"{from_city}, {to_city}, {transport}, {date}"

            result = await request(
                from_city=from_city,
                to_city=to_city,
                transport_type=transport,
                date=date,
            )

            if result and len(result) > 1:
                History.add_command(
                    command="Расписание рейсов по станции",
                    query=query_data,
                    response=result,
                )

                if len(result) > 4096:
                    for count in range(0, len(result), 4096):
                        await message.answer(
                            text=result[count: count + 4095],
                            reply_markup=Buttons.exit_or_again(),
                        )
                else:
                    await message.answer(
                        text=result, reply_markup=Buttons.exit_or_again()
                    )
                logger.success("Result command")

            else:
                logger.error(f"Result {result}")
                await message.answer(
                    cls.info_not_result, reply_markup=Buttons.exit_or_again()
                )

            # await state.finish()

        else:
            await message.reply(text=cls.error_msg_no_sense)

    @classmethod
    async def register_command(cls, dp: Dispatcher) -> None:
        """
        Метод класса регистрирует обработчики сообщений, декораторы.
        Args:
            dp: Передает класс Dispatcher, библиотеке aiogram

        Returns: None

        """
        dp.register_message_handler(
            callback=cls.start_work, text=Buttons.but_command_1.text, state=None
        )
        dp.register_message_handler(
            base_stop_working, Text(Buttons.but_out.text), state="*"
        )
        dp.register_message_handler(
            callback=cls.get_transport_type, state=cls.__transport_type
        )
        dp.register_message_handler(
            callback=cls.get_from_region, state=cls.__form_region
        )
        dp.register_message_handler(callback=cls.get_from_city, state=cls.__from_city)
        dp.register_message_handler(callback=cls.get_to_region, state=cls.__to_region)
        dp.register_message_handler(callback=cls.get_to_city, state=cls.__to_city)
        dp.register_callback_query_handler(
            cls.get_calendar, dialog_cal_callback.filter(), state=cls.__date
        )
        dp.register_message_handler(callback=cls.result, state=cls.__finish)
