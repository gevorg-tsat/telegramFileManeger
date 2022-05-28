from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from db_postgres import sql_bot
from handlers import download


class FSMUser(StatesGroup):
    name = State()
    material = State()


# Старт
# @dp.message_handler(commands='upload', state=None)
async def load_start(message: types.Message):
    await FSMUser.name.set()
    await message.answer('Напишите название материала или отправьте картинку, видео или документ/файл сразу с названием в описании')


# @dp.message_handler(content_types=['text'], state=FSMUser.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await FSMUser.next()
    await message.answer("отправьте материал (текст, картинку, видео или документ/файл)")


async def load_name_and_file(message: types.Message, state: FSMContext):
    if message.caption is None:
        await message.answer('Напишите название материала или отправьте картинку, видео или документ/файл сразу с названием в описании')
        return
    async with state.proxy() as data:
        data['name'] = message.caption
        if message.content_type == 'photo':
            data['material'] = message.photo[0].file_id
            data['data_type'] = 1
        elif message.content_type == 'video':
            data['material'] = message.video.file_id
            data['data_type'] = 2
        else:
            data['material'] = message.document.file_id
            data['data_type'] = 3
    await sql_bot.add_material(state)
    await message.answer("файл загружен")
    await state.finish()
    await load_start(message)


# @dp.message_handler(content_types=['text', 'photo', 'video'], state=FSMUser.material)
async def load_material(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == 'text':
            data['material'] = message.text
            data['data_type'] = 0
        elif message.content_type == 'photo':
            data['material'] = message.photo[0].file_id
            data['data_type'] = 1
        elif message.content_type == 'video':
            data['material'] = message.video.file_id
            data['data_type'] = 2
        else:
            data['material'] = message.document.file_id
            data['data_type'] = 3
    await sql_bot.add_material(state)
    await message.answer("файл загружен")
    await load_start(message)


def register_handlers_load(dp: Dispatcher):
    dp.register_message_handler(load_start, commands='upload', state="*")
    dp.register_message_handler(download.cancel_upload, commands='cancel', state="*")
    dp.register_message_handler(load_name, content_types=['text'], state=FSMUser.name)
    dp.register_message_handler(load_name_and_file, content_types=['photo', 'video', 'document'], state=FSMUser.name)
    dp.register_message_handler(load_material, content_types=['text', 'photo', 'video', 'document'], state=FSMUser.material)