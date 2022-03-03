from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_btn = KeyboardButton(text='❌ Cancel')

cancel_keyboard.add(cancel_btn)