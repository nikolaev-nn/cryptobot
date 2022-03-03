from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import DataBase


db = DataBase()
bot = Bot(token=open('token.txt').readline())
dp = Dispatcher(bot, storage=MemoryStorage())