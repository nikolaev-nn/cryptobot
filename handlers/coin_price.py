import json
from create_bot import bot, dp
from aiogram.types import ParseMode
from aiogram import Dispatcher, types
from coin_data.py import get_crypto_curr
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import main_keyboard, cancel_keyboard
from aiogram.dispatcher.filters.state import State, StatesGroup


class PriceForm(StatesGroup):
    coin = State()


async def command_start(message: types.Message):
    await bot.send_message(message.chat.id, 'Enter the name of the currency in the format BTC, ETH, BNB, LTC', reply_markup=cancel_keyboard)
    await PriceForm.coin.set()


async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, "Let's start from the beginning 😌", reply_markup=main_keyboard)


async def get_coin_price(message: types.Message):
    value = await get_crypto_curr(message.text)
    if value == KeyError:
        await bot.send_message(message.chat.id, 'Currency not found. Check if you entered the currency name correctly.')
    else:
        result = await create_text(message.text.upper(), value)
        text = result[0]
        inline_keyboard = result[1]
        await bot.send_message(message.chat.id, text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    await PriceForm.coin.set()


@dp.callback_query_handler(lambda callback: callback.data == 'refresh info', state='*')
async def refresh_callback(callback: types.CallbackQuery):
    coin_symbol = callback.message.text.split('\n')[0].split()[-1]
    value = await get_crypto_curr(coin_symbol)
    result = await create_text(coin_symbol, value)
    text = result[0]
    inline_keyboard = result[1]
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=inline_keyboard
        )
        await callback.answer()
    except:
        await callback.answer('No changes')


async def create_text(message, value):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup_item = types.InlineKeyboardButton(text="Refresh 🔁", callback_data="refresh info")
    markup.add(markup_item)
    links = json.load(open('./coin_data/templates/crypto_currencies.json'))
    try:
        link = f"{(links[message]['link'])}"
    except:
        link = ''
    text = f"Symbol: <a href='{link}'>{message}</a>\n\n" \
           f"Rank: {value['rank']} \n\n" \
           f"Price: {value['priceValue']:,} $ \n\n" \
           f"Percent Change 24h: {value['percentageChanges']}% {value['emojiPercent']} \n\n" \
           f"Volume Change 24h:  {value['volumeChanges']}% {value['emojiPrice']} \n\n" \
           f"ATH Price: {value['ath_price']} $ \n\n" \
           f"Marketcap: {value['market_cap']:,} 💵 "
    return text, markup


def register_price_handler(dispatcher: Dispatcher):
    dispatcher.register_message_handler(command_start, Text(equals='coin price 💰', ignore_case=True), state=None)
    dispatcher.register_message_handler(cancel_handler, Text(equals='❌ cancel', ignore_case=True), state='*')
    dispatcher.register_message_handler(get_coin_price, state=PriceForm.coin)
