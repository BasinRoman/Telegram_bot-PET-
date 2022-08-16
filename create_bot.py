from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from credentials import bot_token

bot = Bot(token=f"{bot_token}")
dp = Dispatcher(bot, storage=MemoryStorage())











