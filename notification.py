import asyncio
from create_bot import db
from create_bot import bot
from coin_data.py import get_coinpaprika, get_coinex, get_binance, get_bybit, get_gate, get_ftx, get_mexc, get_kucoin


market_dict = {
    'Default': {'method': get_coinpaprika, 'type': 1},
    'Binance': {'method': get_binance, 'type': 0},
    'CoinEx': {'method': get_coinex, 'type': 0},
    'ByBit': {'method': get_bybit, 'type': 0},
    'KuCoin': {'method': get_kucoin, 'type': 0},
    'MEXC': {'method': get_mexc, 'type': 0},
    'FTX': {'method': get_ftx, 'type': 0},
    'Gate': {'method': get_gate, 'type': 0}
}


async def check_coins(user_id):
    current_price_dict = {}
    while True:
        alerts = await db.get_alert(user_id)
        if len(alerts) == 0:
            asyncio.Task.cancel(asyncio.current_task())

        for alert in alerts:
            market = alert[-1]
            coin_type = market_dict[market]['type']
            ticker = alert[coin_type]
            current_price_dict[ticker] = (await market_dict[market]['method'](ticker))
            if alert[3] < alert[2] < current_price_dict[ticker] or alert[3] > alert[2] > current_price_dict[ticker]:
                await bot.send_message(user_id, f'The price of {alert[0]} has reached ${alert[2]}')
                await db.delete_alert([user_id, alert[0], alert[2], market])

        await asyncio.sleep(150)


if __name__ == "__main__":
    pass