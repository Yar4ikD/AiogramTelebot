from config import TOKEN
from aiogram import Bot, Dispatcher


bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
