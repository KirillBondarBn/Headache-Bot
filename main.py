from aiogram.utils import executor
from create_bot import dp
from database import sqlite_db
import os

async def on_startup(_):
    sqlite_db.sql_start()
    print('Bot successfully started')

def delete_report(name):
    os.remove(name)

from handlers import client, admin, other

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)