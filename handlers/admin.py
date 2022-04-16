from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import kb_scale, kb_start
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from database import sqlite_db

class FSMAdmin(StatesGroup):
    scale = State()
    description = State()

async def add_note(message: types.Message):
    await FSMAdmin.scale.set()
    await bot.send_message(message.from_user.id, 'Оцени боль по шкале:', reply_markup=kb_scale)

async def get_desription(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['scale'] = int(message.text)
    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, 'Опиши свой день: ')

async def load_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await sqlite_db.sql_add_command(state, message.from_user.id, message.date, bot, message)
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(add_note, commands=['addnote'], state=None)
    dp.register_message_handler(add_note, Text(equals='Новая запись', ignore_case=True), state=None)
    dp.register_message_handler(get_desription, state=FSMAdmin.scale)
    dp.register_message_handler(load_data, state=FSMAdmin.description)