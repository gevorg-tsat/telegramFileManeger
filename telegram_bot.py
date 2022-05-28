from aiogram import types
from create_bot import dp
from aiogram.utils import executor
from keyboard import keyboard
from db_postgres import sql_bot
from aiogram.dispatcher import FSMContext


async def on_startup(_):
    print("Bot is on")
    sql_bot.sql_start()


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await message.answer("Приветик!", reply_markup=keyboard)
    first = "Для того чтобы добавить материал нажмите /upload, далее вы войдете в режим Загрузки и можете друг за другом загружать материалы по одному\n"
    second = "Чтобы выбрать и получить материал из общего доступа, нажмите /download и вы войдете в режим Выгрузки, и можете по одному выгружать необходимые вам файлы\n"
    third = "Чтобы выйти из любого из режима можете в любой момент нажать /cancel"
    await message.answer(first+second+third)


from handlers import load, download

download.register_handlers_load(dp)
load.register_handlers_load(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
