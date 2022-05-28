from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from db_postgres import sql_bot
from create_bot import dp, bot
from keyboard import keys


class FSMGetMaterial(StatesGroup):
    name = State()


# Старт
# @dp.message_handler(commands='download', state="*")
async def download_start(message: types.Message):
    result = await sql_bot.get_data()
    datatype = ['[Текст]', '[Фото]', '[Видео]', '[Файл/Документ]']
    material_list = 'список материалов:\n'
    for temp in result:
        material_list += (str(temp[0]) + '. ' + temp[1] + ' ' + datatype[int(temp[-1])] + '\n')
    await message.answer(material_list)
    await FSMGetMaterial.name.set()
    await message.answer("Отправьте номер файла, который хотите получить или /отмена для выхода из режима скачивания")


# @dp.message_handler(state=FSMGetMaterial.name)
async def send_material(message: types.Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer('это не номер), введите еще раз')
        return
    material_id = int(message.text)
    result = await sql_bot.get_data_id(material_id)
    if len(result) == 0:
        await message.answer('нет материалов под данным номером, введите еще раз')
        return
    await message.answer('[Материал]:')
    if result[0][-1] == 0:
        await message.answer(result[0][0])
    elif result[0][-1] == 1:
        await message.answer_photo(result[0][0])
    elif result[0][-1] == 2:
        await message.answer_video(result[0][0])
    elif result[0][-1] == 3:
        await message.answer_document(result[0][0])
    await message.answer("Отправьте номер файла, который хотите получить или /cancel для выхода из режима скачивания")
    await FSMGetMaterial.name.set()


async def cancel_upload(message: types.message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("отмена процесса успешно произошла", reply_markup=keys.keyboard)
        return
    await message.answer("отмена процесса успешно произошла", reply_markup=keys.keyboard)
    await state.finish()


def register_handlers_load(dp: Dispatcher):
    dp.register_message_handler(download_start, commands='download', state="*")
    dp.register_message_handler(cancel_upload, commands='cancel', state="*")
    dp.register_message_handler(send_material, state=FSMGetMaterial.name)