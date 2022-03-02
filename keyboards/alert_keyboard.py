from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


alert_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
add_btn = KeyboardButton(text='➕ Add alert')
delete_btn = KeyboardButton(text='🗂 Show alerts')
cancel_btn = KeyboardButton(text='❌ Cancel')

alert_keyboard.add(add_btn).add(delete_btn).add(cancel_btn)

