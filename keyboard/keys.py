from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

button1 = KeyboardButton('/upload')
button2 = KeyboardButton('/download')
button3 = KeyboardButton('/cancel')

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard.add(button1).insert(button2).insert(button3)