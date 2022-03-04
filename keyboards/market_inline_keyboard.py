from aiogram.types import InlineKeyboardButton


# market_markup = InlineKeyboardMarkup(row_width=3)

nomatter_btn = InlineKeyboardButton(text='Default', callback_data='Default')
binance_btn = InlineKeyboardButton(text='Binance', callback_data='Binance')
coinex_btn = InlineKeyboardButton(text='CoinEx', callback_data='CoinEx')
bybit_btn = InlineKeyboardButton(text='ByBit', callback_data='ByBit')
kucoin_btn = InlineKeyboardButton(text='KuCoin', callback_data='KuCoin')
MEXC_btn = InlineKeyboardButton(text='MEXC', callback_data='MEXC')
FTX_btn = InlineKeyboardButton(text='FTX', callback_data='FTX')
gate_btn = InlineKeyboardButton(text='Gate', callback_data='Gate')
cancel_btn = InlineKeyboardButton(text='❌ Cancel', callback_data='cancel market')

market_buttons = [nomatter_btn, binance_btn, FTX_btn, MEXC_btn, bybit_btn, coinex_btn, kucoin_btn, gate_btn]

# market_markup.add(nomatter_btn).row(binance_btn, coinex_btn, bybit_btn).row(kucoin_btn, MEXC_btn, FTX_btn).add(gate_btn).add(cancel_btn)