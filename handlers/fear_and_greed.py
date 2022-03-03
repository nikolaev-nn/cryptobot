import os
import json
import time
import pytz
from create_bot import bot
from datetime import datetime
from aiogram import Dispatcher, types
from coin_data.py import get_crypto_fear
from aiogram.dispatcher.filters import Text


tz_london = pytz.timezone('Europe/London')
datetime_l = datetime.now(tz_london)
current_d = datetime_l.strftime("%Y-%d-%m")
DATE = current_d


async def send_fear_message(message: types.Message):
    try:
        img = open(f'coin_data/{DATE} fear.png', 'rb')
    except Exception:
        await update_fear_index()
        img = open(f'./coin_data/templates/{DATE} fear.png', 'rb')
    fear_data = json.load(open('./coin_data/templates/fear_index.json', 'r'))
    emoji = json.load(open("./coin_data/templates/fear_emoji.json", "rb"))
    current_time = time.localtime()
    time_string1 = time.strftime("%Y/%d/%m", current_time)

    text = f'🚦 Fear & Greed Index Historical Values\n\n' \
           f'{emoji[fear_data["Now"]["status"]]} Now:                   {fear_data["Now"]["num"]} - {fear_data["Now"]["status"]}\n\n' \
           f'{emoji[fear_data["Yesterday"]["status"]]} Yesterday:         {fear_data["Yesterday"]["num"]} - {fear_data["Yesterday"]["status"]}\n\n' \
           f'{emoji[fear_data["Last week"]["status"]]} Last week:          {fear_data["Last week"]["num"]} - {fear_data["Last week"]["status"]}\n\n' \
           f'{emoji[fear_data["Last month"]["status"]]} Last month:       {fear_data["Last month"]["num"]} - {fear_data["Last month"]["status"]}\n\n 📆 Last updated:   {time_string1} \n\n'

    await bot.send_photo(message.chat.id, img, text)


async def update_fear_index():
    global DATE
    try:
        files = os.listdir('coin_data/templates')
        datetime_london = datetime.now(tz_london)
        current_date = datetime_london.strftime("%Y-%d-%m")
        DATE = current_date
        img_dates = [img_file for img_file in files if 'fear.png' in img_file]
        if len(img_dates) == 0:
            await get_crypto_fear(current_date=current_date)

        last_date = img_dates[0].split()[0]
        if last_date != current_date:
            await get_crypto_fear(current_date=current_date)
            os.remove(f"coin_data/templates/{last_date} fear.png")
            print('fear-coin_data updated')

    except KeyboardInterrupt:
        pass


def register_fear_handler(dispatcher: Dispatcher):
    dispatcher.register_message_handler(send_fear_message, Text(equals='fear & greed 🚦', ignore_case=True))
