import asyncio
from aiogram import types

from coin_data.py import get_member_status
from create_bot import dp, bot, db, chat_id
from aiogram.utils import executor

from notification import check_coins
from keyboards import main_keyboard
from handlers import coin_price, price_alert, fear_and_greed, funding_rates


async def on_startup(_):
    print('Bot is online!')
    users_id = set(await db.get_users_id())
    for user_id in users_id:
        asyncio.Task(check_coins(user_id[0])).set_name(user_id[0])


@dp.message_handler(commands=['start'])
async def start_func(message: types.Message):
    user_status = await get_member_status(message)
    if user_status:
        await db.add_user((message.from_user.id, message.from_user.username, message.from_user.first_name))
        await bot.send_message(message.chat.id, "Hi! I am a crypto bot. With my help, you can easily find out about the current state of the cryptocurrency"
                                                "you are interested in.", reply_markup=main_keyboard)


coin_price.register_price_handler(dp)
fear_and_greed.register_fear_handler(dp)
price_alert.register_alert_handler(dp)
funding_rates.register_funding_rates_handler(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
