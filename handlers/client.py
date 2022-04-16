from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from keyboards import kb_start, kb_scale
from database import sqlite_db

async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, '/help - Информация о всех командах\n/addnote - Добавить запись\n/clearnotes - Очистить информацию о себе\n/makereport - Просмотреть все записи', reply_markup=kb_start)

async def make_report(message: types.Message):
    await sqlite_db.sql_read(message, message.from_user.id)

async def remove_notes(message: types.Message):
    await sqlite_db.sql_remove(message, message.from_user.id)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(remove_notes, commands=['clearnotes'])
    dp.register_message_handler(remove_notes, Text(equals='Стереть записи', ignore_case=True))
    dp.register_message_handler(make_report, commands=['makereport'])
    dp.register_message_handler(make_report, Text(equals="Составить отчёт", ignore_case=True))