import asyncio
from create_bot import db
from create_bot import bot
from coin_data.py import get_coin_data


async def check_coins(user_id):
    current_price_dict = {}
    while True:
        alerts = await db.get_alert(user_id)
        print('It works, ---', user_id, alerts)
        tickers = set([ticker[1] for ticker in alerts])
        for ticker in tickers:
            current_price_dict[ticker] = (await get_coin_data(ticker))['quotes']['USD']['price']
        for alert in alerts:
            if alert[3] < alert[2] < current_price_dict[alert[1]]:
                await bot.send_message(user_id, f'The price of {alert[0]} has reached $ {alert[2]}')
                await db.delete_alert([user_id, alert[0], alert[2]])

            elif alert[3] > alert[2] > current_price_dict[alert[1]]:
                await bot.send_message(user_id, f'The price of {alert[0]} has reached $ {alert[2]}')
                await db.delete_alert([user_id, alert[0], alert[2]])

        await asyncio.sleep(180)


if __name__ == "__main__":
    pass
