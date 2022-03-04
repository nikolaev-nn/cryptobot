from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


sub_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
cancel_btn = InlineKeyboardButton(text='✅ Check', callback_data='check')

sub_keyboard.add(cancel_btn)