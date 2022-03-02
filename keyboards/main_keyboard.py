from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
rate_btn = KeyboardButton(text='Coin price 💰')
notif_btn = KeyboardButton(text='Price alert 📈')
fear_btn = KeyboardButton(text='Fear & Greed 🚦')

main_keyboard.row(rate_btn, notif_btn).add(fear_btn)
