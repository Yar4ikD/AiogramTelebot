from aiogram import types, Dispatcher
from aiogram.types import ContentType, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboard.list_nearest_buttons import button_location, button_stations_type, button_distance, add_distance
from api.get_list_nearest_stations import get_nearest_stations


class StationFSM(StatesGroup):
    location = State()
    type_station = State()
    distance = State()
    limit = State()


async def start_work(callback: types.CallbackQuery, state: FSMContext) -> None:

    info = f'{callback.message.chat.first_name}, для получения списка ближайших станций вам нужно указать Геолокацию'

    await StationFSM.location.set()
    await callback.message.answer(text=info, reply_markup=button_location())
    await callback.answer()


async def location(message: types.Message, state: FSMContext) -> None:

    if message.location:
        async with state.proxy() as data:
            data['lat'] = message.location.latitude
            data['lng'] = message.location.longitude

        info = 'Выберите тип станции:'
        await StationFSM.next()
        await message.answer(text=info, reply_markup=button_stations_type())

    else:
        info = 'Я не понимаю, что это значит?' \
               '\nЭто точно не ваша геолокация!\nПередайте мне геолокацию, для дальнейшей работы!'
        await message.reply(text=info, reply_markup=button_location())


async def station(callback: [types.CallbackQuery, types.Message], state: FSMContext) -> None:
    print('station')

    if isinstance(callback, CallbackQuery):
        info = 'Укажите радиус поиска'
        async with state.proxy() as data:
            data['station'] = callback.data

        await StationFSM.next()
        await callback.message.answer(text=info, reply_markup=button_distance())

    else:
        info = '<b>Выберите один вариант из списка.</b>\n<b>Не нужно</b> писать сообщение!\nОтправляю список повторно:'
        await callback.reply(text=info, reply_markup=button_stations_type())


async def radius(callback: types.CallbackQuery, state: FSMContext) -> None:
    print('radius')

    if callback.data:
        async with state.proxy() as data:
            result = await get_nearest_stations(
                lat=data.get('lat'), lng=data.get('lng'), station_type=data.get('station'), distance=callback.data)

        if result:
            await callback.message.answer(text=result)
            await StationFSM.first()
        else:
            info = 'В данном радиусе поиска нет станций, по вашему запросу.' \
                   '\nПопробуйте увеличить радиус.'

            await callback.message.answer(text=info, reply_markup=add_distance())


async def register_command_nearest_station(dp: Dispatcher) -> None:

    dp.register_callback_query_handler(callback=start_work, text='nearest_list', state=None)
    dp.register_message_handler(callback=location, content_types=[ContentType.LOCATION, ContentType.TEXT],
                                state=StationFSM.location
                                )
    dp.register_callback_query_handler(callback=station, state=StationFSM.type_station)
    dp.register_message_handler(callback=station, state=StationFSM.type_station)
    dp.register_callback_query_handler(callback=radius, state=StationFSM.distance)