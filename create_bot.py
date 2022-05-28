from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=MemoryStorage())