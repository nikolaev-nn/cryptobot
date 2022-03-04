import json
import asyncio
import os
import pickle

from typing import Union

from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from coin_data.py import get_member_status
from notification import check_coins
from create_bot import bot, db, dp, chat_id
from coin_data.py import get_ticker, get_coin_data
from keyboards import main_keyboard, alert_keyboard, cancel_keyboard, market_buttons, cancel_btn

from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton


class AlertForm(StatesGroup):
    coin_name = State()
    coin_price = State()
    market = State()


@dp.callback_query_handler(lambda callback: callback.data == 'cancel market', state=AlertForm.market)
async def cancel_handler(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    await state.finish()
    if type(message) == types.Message:
        chat_id_2 = message.chat.id
    else:
        chat_id_2 = message.message.chat.id
        message_id = message.message.message_id
        await bot.delete_message(chat_id_2, message_id)
    await bot.send_message(chat_id_2, "Let's start from the beginning 😌", reply_markup=main_keyboard)
    await message.answer()


async def select_alert(message: types.Message):
    user_status = await get_member_status(message)
    if user_status:
        await bot.send_message(message.chat.id, "Select:", reply_markup=alert_keyboard)


async def create_alert(message: types.message):
    user_status = await get_member_status(message)
    if user_status:
        await AlertForm.coin_name.set()
        await bot.send_message(message.chat.id, 'Type the name of the currency (BTC, ETH, BNB)', reply_markup=cancel_keyboard)


async def set_coin_name_invalid(message: types.Message):
    return await message.reply("No currency with this name was found 😕")


async def set_coin_name(message: types.Message, state: FSMContext):
    user_status = await get_member_status(message)
    if user_status:
        async with state.proxy() as data:
            data['coin_name'] = message.text.upper()
            data['coin_ticker'] = await get_ticker(message.text.upper())
        await AlertForm.next()
        await bot.send_message(message.chat.id, 'Enter the price at which the bot will notify you.'
                                                '\n\nIf the number is not an integer, then enter it separated by a dot. For example:\n\n- 0.2\n- 10.5\n- 8.40')


async def set_coin_price_invalid(message: types.Message):
    return await message.reply("The price was entered incorrectly 😕 Try again")


async def set_coin_price(message: types.Message, state: FSMContext):
    user_status = await get_member_status(message)
    if user_status:
        async with state.proxy() as data:
            data['coin_price'] = message.text
            data['last_price'] = (await get_coin_data(data['coin_ticker']))['quotes']['USD']['price']
            keyboard = await create_market_keyboard(get_markets(data['coin_name']))
            await bot.send_message(message.chat.id, f"Now choose coin market", reply_markup=keyboard)
        await AlertForm.next()


@dp.callback_query_handler(lambda callback: callback.data.lower() in ['binance', 'coinex', 'bybit', 'kucoin', 'mexc', 'ftx', 'gate', 'default'], state=AlertForm.market)
async def set_market(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['market'] = call.data
        data['user_id'] = call.from_user.id
        tasks = [t.get_name() for t in asyncio.all_tasks()]
        await db.save_alert(data)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        if str(call.message.chat.id) not in tasks:
            user_id = call.message.chat.id
            asyncio.Task(check_coins(user_id)).set_name(user_id)

        await bot.send_message(call.message.chat.id, f"That's it! The bot will notify you when the {data['coin_name']} price reaches ${data['coin_price']}",
                               reply_markup=main_keyboard)
    await state.finish()


async def show_alerts(message: types.Message):
    user_status = await get_member_status(message)
    if user_status:
        await list_alerts(message, message.chat.id)


@dp.callback_query_handler(lambda callback: callback.data.split('#')[0] == 'elements', state='*')
async def pagination_callback(call: types.CallbackQuery):
    page = int(call.data.split('#')[1])
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await list_alerts(call, call.message.chat.id, page)
    await call.answer()


@dp.callback_query_handler(lambda callback: callback.data == 'delete alert', state='*')
async def delete_alert_callback(call: types.CallbackQuery):
    callback_text = call.message.text.split('\n\n')
    coin = callback_text[0].split()[1]
    price = callback_text[1].split()[1].replace('$', '').replace(',', '')
    market = callback_text[2].split()[1]
    await db.delete_alert([call.message.chat.id, coin, price, market])
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await call.answer(f'The ${price} {coin} alert has been deleted!')
    await list_alerts(call, call.message.chat.id)
    await call.answer()


async def list_alerts(message: Union[types.Message, types.CallbackQuery], chat_id_2, page=1):
    pages = await db.show_alerts(message.from_user.id)
    if len(pages) == 0:
        await bot.send_message(chat_id_2, 'There is no alert!')
    else:
        paginator = InlineKeyboardPaginator(
            len(pages),
            current_page=page,
            data_pattern='elements#{page}'
        )
        paginator.add_before(InlineKeyboardButton('Delete alert', callback_data='delete alert'))
        coin_info = pages[page - 1]
        text = f"Symbol: {coin_info[0]}\n\nPrice: ${coin_info[1]:,}\n\nMarket: {coin_info[2]}"
        await bot.send_message(
            chat_id_2,
            text,
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )


def register_alert_handler(dispatcher: Dispatcher):
    dispatcher.register_message_handler(cancel_handler, Text(equals='❌ Cancel', ignore_case=True), state='*')
    dispatcher.register_message_handler(select_alert, Text(equals='Price alert 📈', ignore_case=True))
    dispatcher.register_message_handler(create_alert, Text(equals='➕ Add alert', ignore_case=True))
    dispatcher.register_message_handler(set_coin_name_invalid, lambda message: len(get_markets(message.text.upper())) == 0, state=AlertForm.coin_name)
    dispatcher.register_message_handler(set_coin_name, state=AlertForm.coin_name)
    dispatcher.register_message_handler(set_coin_price_invalid, lambda message: not isfloat(message.text), state=AlertForm.coin_price)
    dispatcher.register_message_handler(set_coin_price, state=AlertForm.coin_price)
    dispatcher.register_message_handler(show_alerts, Text(equals='🗂 Show alerts', ignore_case=True))


def get_markets(coin_name):
    direction = 'coin_data/templates/coin_symbols/'
    files = os.listdir(direction)
    markets = []
    for file in files:
        if file == 'coin_names.json':
            if coin_name in json.load(open(f'{direction}{file}', 'r')).values():
                markets.append('Default')
        elif '.pkl' in file:
            if coin_name in pickle.load(open(f'{direction}{file}', 'rb')):
                markets.append(file.split('.')[0])
    return markets


async def create_market_keyboard(markets):
    kb = InlineKeyboardMarkup(row_width=3)
    for btn in market_buttons:
        if btn.text in markets:
            kb.add(btn)
    return kb.row(cancel_btn)


def isfloat(message):
    try:
        float(message)
        return True
    except:
        return False
