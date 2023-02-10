"""
    Модуль работы команды ТГ-бота: Расписание рейсов по станции.
"""

import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram_calendar import dialog_cal_callback, DialogCalendar
from database.select_data_for_command.station_timetable import Select
from keyboard.station_timetable_buttons import Buttons
from api.get_schedule_station import request
from loguru import logger
from .base_command import base_stop_working

# base_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(base_dir, '../database', '../loader.py'))
#
# from loader import dp, bot


class Command(StatesGroup):
    """
        Подкласс наследует от базового класса StatesGroup.
        В классе прописана работа команды ТГ-бота: Расписание рейсов по станции.
        Приватные атрибуты класса это FSM состояние ТГ-бота.
    """
    __event_and_transport = State()
    __region = State()
    __settlement = State()
    __station_code = State()
    __dat = State()
    __result = State()

    info_start = f'{emoji.emojize(":trolleybus:")} Выберите тип транспорта и направление'
    info_region = 'Укажите <b>названия области</b>, без добавления: <b>обл, рег</b> Пример:\n' \
                  '<b>Ярославская</b>\n<b>Московская</b>\n<b>Псковская</b>'
    info_settlement = f'Укажите название населенного пункта {emoji.emojize(":backhand_index_pointing_down:")}'
    info_station = f'Укажите название станции {emoji.emojize(":backhand_index_pointing_down:")}'
    info_date = f'Укажите дату {emoji.emojize(":calendar:")}'
    info_result = 'По вашему запросу найдено:'
    msg_error_region = f'Я не нашел в базе такой области.' \
                       f'\nПопробуйте еще раз {emoji.emojize(":backhand_index_pointing_down:")}'
    msg_error_sett = 'Я не нашел в базе такого населенного пункта.\nУкажите название еще раз...'
    msg_error_list_st = 'К сожалению в этом населенном пункте, нет станций!'
    msg_error_station = 'Я не нашел в базе такой станции.\nУкажите название еще раз...'
    error_msg_no_sense = f'Что это значить, я не понимаю Вас{emoji.emojize(":person_shrugging:")}' \
                         f'\nВыберите одну из команд.'

    data_keys = ('region', 'city', 'station_code', 'transport', 'event', 'date')

    @classmethod
    async def start(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса запускает процесс работы команды ТГ-бота: Расписание рейсов по станции.
        Запускает машинное состояние бота - FSM __event_and_transport.
        Выводит пользователю информацию о дальнейшем взаимодействии, пользователя с командой ТГ-бота.

        Args:
            message: Передает объект - входящий запрос обратного вызова с кнопки
            state: Передает класс FSM состояния бота.

        Returns: None

        """
        logger.info(f'User id > {message.from_user.id} start command {message.text}')
        await cls.__event_and_transport.set()  # запускаем FSM состояния бота
        await message.answer(text=cls.info_start, reply_markup=Buttons.event_transport())

    @classmethod
    @logger.catch()
    async def _universal(cls, message: types.Message, state: FSMContext, data_key: str = None,
                         flag: str = None, reg_code: str = None, sett_code: str = None, transport: str = None,
                         msg_cont: str = None, msg_error: str = None, msg_step_back: str = None,
                         markup_back=Buttons.tru_continue(),
                         markup: ReplyKeyboardMarkup = ReplyKeyboardRemove()) -> None:
        """
        Метод класса для обработки сообщений от пользователя.
        Является универсальным обработчиком для 3х состояний бота:
            __region
            __settlement
            __station_code
        Args:
            message: Передает сообщение от пользователя
            state: Передает FSM состояние
            data_key: Передает ключ из кортежа data_keys
            flag: Передает ключ из кортежа data_keys, является флагом для вариантов запроса к БД
            reg_code: Передает код региона
            sett_code: Передает код населенного пункта
            transport: Передает тип транспорта
            msg_cont: Передает сообщение, инструкцию для дальнейше работы с командой бота
            msg_error: Передает сообщение, которое возвращается пользователю
            msg_step_back: Передает сообщение, инструкцию работы, предыдущим FSM состояния бота
            markup_back: Передает кнопки бота, предыдущего раздела
            markup: Передает кнопки бота.

        Returns: None
        """

        if message.text == Buttons.but_continue.text:  # подтверждение ввода данных, продолжение работы команды
            await cls.next()  # переключает FSM состояния
            await message.answer(text=msg_cont, reply_markup=markup)
            await message.delete()

        elif message.text == Buttons.but_step_back.text:  # возвращаем бота в предыдущее FSM состояния
            await cls.previous()
            await message.answer(text=msg_step_back, reply_markup=markup_back)
            await message.delete()

        elif message.text == Buttons.but_list_stations.text:  # выводит список станций в населенном пункте
            async with state.proxy() as data:
                c_code, tr_code = data.get(cls.data_keys[1]), data.get(cls.data_keys[3])
            response = await Select.list_station(settlement_code=c_code, transport=tr_code)

            if response:
                await message.answer(text=response)
            else:
                await message.reply(text=cls.msg_error_list_st)

        else:
            user_msg = message.text.capitalize().strip()  # обработка сообщения от пользователя

            if flag == cls.data_keys[1]:  # ищет населенный пункт в БД
                response = await Select.settle(user_msg=user_msg, region_code=reg_code)

            elif flag == cls.data_keys[2]:  # ищет станцию и яндекс код в БД
                response = await Select.yandex_code(user_msg=user_msg, settlement=sett_code, transport_type=transport)

            else:  # ищет регион в БД
                response = await Select.select_region(user_msg=user_msg)

            if response and len(response[1]) > 2:

                info = f'Вот что я нашел:\n<b>{response[1]}\n</b>Если все правильно, нажмите ' \
                       f'<b>{Buttons.but_continue.text}</b>\nВ противном случае укажете данные заново!'

                async with state.proxy() as data:
                    data[data_key] = response[0]  # записываем код из БД

                await message.reply(text=info, reply_markup=Buttons.tru_continue())
                # await message.delete()
            else:
                await message.reply(text=msg_error, reply_markup=Buttons.output())

    @classmethod
    @logger.catch()
    async def get_event_and_type_transport(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса обработчик, принимает от пользователя: Тип транспорта, прибытие или отправление.
        Записывает ответ и переключает FSM состояние на __region.
        Args:
            message: Передает сообщение от пользователя
            state: Передает FSM состояние бота, __event_and_transport.

        Returns: None
        """
        if message.text in Buttons.event_and_transport:
            value = Buttons.event_and_transport.get(message.text)

            async with state.proxy() as data:
                data['transport'], data['event'] = value
            await cls.next()
            await message.answer(text=cls.info_region, reply_markup=ReplyKeyboardRemove())
        else:
            await message.reply(text=cls.error_msg_no_sense, reply_markup=Buttons.event_transport())

    @classmethod
    async def region(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса обрабатывает данные от пользователя, название региона.
        Делает запрос к БД, для получения код региона, указанного пользователем.
        Вызывает FSM состояние бота - получения код населенного пункта.
        Вызывает универсальный метод и передает в качестве аргументов, данные полученные от пользователя.
        Args:
            message: Передает название региона
            state: Передает FSM состояние бота, __region.

        Returns: None
        """
        key = cls.data_keys[0]
        await cls._universal(message=message, state=state, data_key=key, msg_cont=cls.info_settlement,
                             msg_step_back=cls.info_start, msg_error=cls.msg_error_region,
                             markup_back=Buttons.event_transport())

    @classmethod
    async def settlement(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса обрабатывает данные от пользователя, название населенного пункта.
        Делает запрос к БД, для получения код населенного пункта, указанного пользователем.
        Вызывает FSM состояние бота - получения код станции.
        Вызывает универсальный метод и передает в качестве аргументов, данные полученные от пользователя.
        Args:
            message: Передает название населенного пункта
            state: Передает FSM состояние бота, __settlement.

        Returns: None
        """

        key = cls.data_keys[1]
        async with state.proxy() as data:
            reg_code = data.get(cls.data_keys[0])

        await cls._universal(message=message, state=state, flag=key, data_key=key, reg_code=reg_code,
                             msg_step_back=cls.info_region, msg_cont=cls.info_station, msg_error=cls.msg_error_sett,
                             markup=Buttons.show_list())

    @classmethod
    async def station(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса обрабатывает данные от пользователя, название станции.
        Делает запрос к БД, для получения код станции, которую указал пользователь.
        Вызывает FSM состояние бота - получения даты.
        Вызывает универсальный метод и передает в качестве аргументов, данные полученные от пользователя.
        Вызывает класс DialogCalendar().start_calendar() для отправки в чат виджет календарь.
        Args:
            message: Передает название станции
            state: Передает FSM состояние бота, __station_code

        Returns:
        """
        key = cls.data_keys[2]
        async with state.proxy() as data:
            reg_code, city_code = data.get(cls.data_keys[0]), data.get(cls.data_keys[1])
            transport = data.get(cls.data_keys[3])

        await cls._universal(message=message, state=state, flag=key, data_key=key, reg_code=reg_code,
                             sett_code=city_code, transport=transport, msg_cont=cls.info_date,
                             msg_step_back=cls.info_settlement,
                             msg_error=cls.msg_error_station,
                             markup=await Buttons.calendar().start_calendar())  #  await DialogCalendar().start_calendar())

    @classmethod
    async def get_calendar(cls, callback_query: types.CallbackQuery,
                           callback_data: CallbackData, state: FSMContext) -> None:
        """
        Метод класса, обрабатывает данные виджета календаря.
        Переводит FSM бота в состояние __result.

        Args:
            callback_query: Передает кнопки календаря
            callback_data: Передает данные кнопок календаря
            state: Передает FSM состояние бота, __dat.

        Returns: None

        """

        if isinstance(callback_query, types.CallbackQuery):
            selected, date = await Buttons.calendar().process_selection(callback_query, callback_data)
            if selected:
                await callback_query.message.answer(f'Указанная вами дата: <b>{date.strftime("%Y-%m-%d")}</b>',
                                                    reply_markup=Buttons.tru_continue())
                async with state.proxy() as data:
                    data['date'] = date.strftime("%Y-%m-%d")
                await cls.next()

    @classmethod
    @logger.catch()
    async def result(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод обработчик, возвращает пользователю информацию запроса.
        Останавливает FSM состояние команды бота.
        Завершает работу команды ТГ-бота.

        Args:
            message: Передает сообщение от пользователя
            state: Передает FSM состояние бота, __result.

        Returns: None
        """
        if message.text == Buttons.but_step_back.text:  # возвращаем бота в предыдущее FSM состояния
            await cls.previous()
            await message.answer(text=cls.info_date, reply_markup=await DialogCalendar().start_calendar())

        elif message.text == Buttons.but_continue.text:  # выводим ответ пользователю на его запрос.

            async with state.proxy() as data:
                code, date = data.get(cls.data_keys[2]), data.get('date')
                transport, event = data.get('transport_type'), data.get('event')

            result = await request(station_code=code, date=date, transport=transport, event=event)

            if result and len(result) > 1:
                if len(result) > 4096:
                    for count in range(0, len(result), 4096):
                        await message.answer(text=result[count: count + 4095], reply_markup=Buttons.button_result())
                else:
                    await message.answer(text=result, reply_markup=Buttons.button_result())
            else:
                not_result = 'По Вашему запросу нет информации.'
                await message.answer(not_result, reply_markup=Buttons.button_result())

            await state.finish()

        else:
            await message.reply(text=cls.error_msg_no_sense)

    @classmethod
    async def register_command(cls, dp: Dispatcher):
        """
        Метод класса регистрирует обработчики сообщений, декораторы.
        Args:
            dp: Передает класс Dispatcher, библиотеке aiogram

        Returns: None

        """
        dp.register_message_handler(callback=cls.start, text=Buttons.but_command_2.text, state=None)
        dp.register_message_handler(base_stop_working, Text(Buttons.but_out_k.text), state='*')
        dp.register_message_handler(callback=cls.get_event_and_type_transport, state=cls.__event_and_transport)
        dp.register_message_handler(callback=cls.region, state=cls.__region)
        dp.register_message_handler(callback=cls.settlement, state=cls.__settlement)
        dp.register_message_handler(callback=cls.station, state=cls.__station_code)
        dp.register_callback_query_handler(cls.get_calendar, dialog_cal_callback.filter(), state=cls.__dat)
        dp.register_message_handler(callback=cls.result, state=cls.__result)
