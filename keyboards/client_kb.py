from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_add_note = KeyboardButton('Новая запись')
button_make_report = KeyboardButton('Составить отчёт')
button_remove_notes = KeyboardButton('Стереть записи')

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add(button_add_note).row(button_make_report, button_remove_notes)

kb_scale = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton('1')
b2 = KeyboardButton('2')
b3 = KeyboardButton('3')
b4 = KeyboardButton('4')
b5 = KeyboardButton('5')
b6 = KeyboardButton('6')
b7 = KeyboardButton('7')
b8 = KeyboardButton('8')
b9 = KeyboardButton('9')
b10 = KeyboardButton('10')
kb_scale.row(b1, b2, b3, b4, b5, b6, b7, b8, b9, b10)