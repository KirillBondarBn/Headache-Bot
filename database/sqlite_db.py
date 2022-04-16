import sqlite3 as sq
from create_bot import dp, bot
from keyboards import kb_start
from xls_reports import xls_creator
from aiogram.types import InputFile

def sql_start():
    global base, cur
    base = sq.connect('headache_data.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS data(id INTEGER, user_id INTEGER, time DATE, scale INTEGER, description TEXT)')
    base.commit()

async def sql_add_command(state, user_id, date, bot, message):
    async with state.proxy() as data:
        abc = list(data.values())
        current_values = (user_id, date, abc[0], abc[1])
        cur.execute('INSERT INTO data VALUES (?, ?, ?, ?)', current_values)
        await bot.send_message(message.from_user.id, 'Запись добавлена', reply_markup=kb_start)
        print(str(date) + ': Note for user ' + str(user_id) + ' successfully added')
        base.commit()

async def sql_read(message, user_id):
    summ = cnt =0
    list_of_notes = []
    try:
        try:
            for ret in cur.execute('SELECT * FROM data WHERE user_id='+str(user_id)).fetchall():
                list_of_notes.append(ret)
                cnt += 1
                summ += int(ret[2])
        except:
            await bot.send_message(message.from_user.id, 'Похоже вы ещё не оставили ни одной записи')
        xls_creator.create_report(list_of_notes, message.from_user.id)
        file = InputFile(str(message.from_user.id)+'_report.xls')
        file.filename = str(message.from_user.id)+'_report.xls'
        await bot.send_document(message.chat.id, file)
        xls_creator.delete_report(str(message.from_user.id)+'_report.xls')

        output = 'Среднее значение боли: ' + str(summ / cnt)[0:4]
        await bot.send_message(message.from_user.id, output)

        print('Report for ' + str(message.from_user.id) + ' has done')
    except:
        await bot.send_message(message.from_user.id, 'Произошла непредвиденная ошибка')

async def sql_remove(message, user_id):
    try:
        sql_query = "DELETE FROM data WHERE user_id="+str(user_id)
        cur.execute(sql_query)
        await bot.send_message(message.from_user.id, 'Записи успешно удалены')
        print(str(message.date) + ' ' + str(user_id) + ' notes was deleted')
        base.commit()
    except:
        await bot.send_message(message.from_user.id, 'Похоже вы ещё не оставили ни одной записи')