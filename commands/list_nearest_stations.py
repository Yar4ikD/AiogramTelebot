"""
    В этом модуле прописана логика работы команды ТГ-бота: Список ближайших станций.
"""
import emoji
from aiogram import types, Dispatcher
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboard.list_nearest_buttons import Buttons
from api.get_list_nearest_stations import request
from database.user_request_history.work_with_db import History
from loguru import logger


class Command(StatesGroup):
    """
        Подкласс наследует от базового класса StatesGroup.
        В классе прописана работа команды ТГ-бота: Список ближайших станций.
        Приватные атрибуты класса это FSM состояние ТГ-бота.
    """
    __location = State()
    __type_station = State()
    __distance = State()
    __end = State()

    info_start = f'Для получения списка ближайших станций укажите геолокацию.'
    info_select_type_stat = 'Выберите тип станции:'
    info_radius = f'Укажите радиус поиска в км{emoji.emojize(":backhand_index_pointing_down:")}'
    conf_radius = f'Если все правильно, нажмите <b>{Buttons.but_continue.text}</b>' \
                  f'\nВ противном случае укажите радиус заново!'
    error_location = 'Я не понимаю, что это значит?\nЭто точно не ваша геолокация!' \
                     '\nПередайте мне геолокацию, для дальнейшей работы!'
    error_type_station = '<b>Выберите один вариант из списка.</b>\n<b>Не нужно</b> писать сообщение!' \
                         '\nОтправляю список повторно:'
    error_radius = '<b>Выберите один вариант из списка.</b>\nИли укажи число!\nОтправляю список повторно.'
    error_result = 'В данном радиусе поиска нет станций, по вашему запросу.\nМакс радиус поиска 50 км.'

    @classmethod
    async def start(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса запускает процесс работы команды ТГ-бота.
        Запускает машинное состояние бота - FSM __location.
        Выводит в чат телеграмма, инструкцию о дальнейшем взаимодействии, пользователя с командой ТГ-бота.
        Args:
            message: Передает сообщения
            state: Передает FSM состояние бота, None.

        Returns: None

        """
        logger.info(f'User id: {message.from_user.id} | command: {message.text}')
        await cls.__location.set()
        await message.answer(text=cls.info_start, reply_markup=Buttons.location())

    @classmethod
    async def location(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса обрабатывает координаты локации пользователя.
        Переключает FSM состояние на __type_station.
        Args:
            message: Передает координаты местонахождения пользователя
            state: Передает FSM состояние бота, __location.

        Returns: None

        """
        if message.location:
            async with state.proxy() as data:
                data['lat'], data['lng'] = message.location.latitude, message.location.longitude
            await cls.next()
            await message.answer(text=cls.info_select_type_stat, reply_markup=Buttons.stations_type())

        else:
            await message.reply(text=cls.error_location, reply_markup=Buttons.location())

    @classmethod
    async def station(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса обрабатывает информацию о типе станции для поиска.
        Переключает FSM состояние на __distance.
        Args:
            message: Передает тип станции
            state: Передает FSM состояние бота, __type_station.

        Returns: None

        """
        if message.text in Buttons.but_stations_type:
            async with state.proxy() as data:
                data['station'] = Buttons.but_stations_type.get(message.text)

            logger.info(f'Enter type station: {message.text}')
            await cls.next()
            await message.answer(text=cls.info_radius, reply_markup=Buttons.distance())

        elif message.text == Buttons.but_step_back.text:  # возвращаем бота в предыдущее FSM состояния
            await cls.previous()
            await message.reply(text=cls.info_start, reply_markup=Buttons.location())

        else:
            await message.reply(text=cls.error_type_station, reply_markup=Buttons.stations_type())

    @classmethod
    async def radius(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса обрабатывает информацию о радиусе поиска.
        Переключает FSM состояние на __end.
        Args:
            message: Передает радиус поиска в км
            state: Передает FSM состояние бота, __distance.

        Returns: None

        """
        if message.text.isnumeric() or message.text in Buttons.buttons_distance:  # является ли сообщения числом(int)
            async with state.proxy() as data:
                data['radius'] = int(message.text)

            logger.info(f'Enter radius: {message.text}')
            await cls.next()
            await message.reply(text=cls.conf_radius, reply_markup=Buttons.tru_continue())

        elif message.text == Buttons.but_step_back.text:  # возвращаем бота в предыдущее FSM состояния
            await cls.previous()
            await message.reply(text=cls.info_select_type_stat, reply_markup=Buttons.stations_type())

        else:
            await message.reply(text=cls.error_radius, reply_markup=Buttons.distance())

    @classmethod
    async def result(cls, message: types.Message, state: FSMContext) -> None:
        """
        Метод класса обработчик, возвращает пользователю информацию запроса.
        Останавливает FSM состояние команды бота.
        Завершает работу команды ТГ-бота.
        Args:
            message: Передает сообщение от пользователя
            state: Передает FSM состояние бота, __end.

        Returns: None

        """
        if message.text == Buttons.but_step_back.text:  # возвращаем бота в предыдущее FSM состояния

            await cls.previous()
            await message.reply(text=cls.info_radius, reply_markup=Buttons.distance())

        elif message.text == Buttons.but_continue.text:
            async with state.proxy() as data:
                lat, lng = data.get('lat'), data.get('lng')
                station_type, distance = data.get('station'), data.get('radius')
                query_data = f'{lat}, {lng}, {station_type}, {distance}'

                result = request(lat=lat, lng=lng, station_type=station_type, distance=distance)

            if result:
                History.add_command(command='Список ближайших станций', query=query_data, response=result)

                await message.answer(text=result, reply_markup=Buttons.result())
                # await state.finish()
                logger.success('Result command')

            else:
                logger.error(f'Result {result}')
                await message.answer(text=cls.error_result, reply_markup=Buttons.result())

    @classmethod
    async def register_command(cls, dp: Dispatcher) -> None:
        """
        Метод класса регистрирует обработчики сообщений, декораторы.
        Args:
            dp: Передает класс Dispatcher, библиотеке aiogram
        Returns: None

        """
        dp.register_message_handler(callback=cls.start, text=Buttons.but_command_3.text, state=None)
        dp.register_message_handler(callback=cls.location, content_types=[ContentType.LOCATION, ContentType.TEXT],
                                    state=cls.__location)
        dp.register_message_handler(callback=cls.station, state=cls.__type_station)
        dp.register_message_handler(callback=cls.radius, state=cls.__distance)
        dp.register_message_handler(callback=cls.result, state=cls.__end)
