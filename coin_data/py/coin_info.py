import requests
import asyncio
import json

from os import path

direction = path.dirname(path.abspath(__file__))


async def get_coin_symbols():
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, f'https://api.coinpaprika.com/v1/tickers/')
    coins_json = json.loads(response.text)
    symbols_dict = {}
    for coin in coins_json:
        symbols_dict[coin['id']] = coin['symbol']
    with open(path.join(direction, '../templates/coin_symbols/coin_names.json'), 'w') as file:
        json.dump(symbols_dict, file, indent=3)


async def get_ticker(currency):
    with open(path.join(direction, '../templates/coin_symbols/coin_names.json'), 'r') as file:
        coins_data = json.load(file)
        for coin, value in coins_data.items():
            if currency.upper() == value:
                return coin
        file.close()


async def get_coin_data(ticker):
    loop = asyncio.get_event_loop()
    request = loop.run_in_executor(None, requests.get, f'https://api.coinpaprika.com/v1/tickers/{ticker}')
    return json.loads((await request).text)


async def check_price_format(price):
    price_split = str(price).split('.')
    if len(price_split) == 2:
        if price_split[0][0] != '0' and len(price_split[0]) > 1:
            price = round(price, 3)
        else:
            price = round(price, 8)
    return price


async def get_crypto_curr(curr):
    ticker = await get_ticker(curr)
    if ticker is None:
        return KeyError
    coin_info = await get_coin_data(ticker)
    if str(coin_info['quotes']['USD']['volume_24h_change_24h'])[0] != '-':
        emoji = '🟢'
    else:
        emoji = '🔴'

    if str(coin_info['quotes']['USD']['percent_change_24h'])[0] != '-':
        emoji_percent = '🟢'
    else:
        emoji_percent = '🔴'

    price = await check_price_format(coin_info['quotes']['USD']['price'])
    data = {
        'priceValue': price,
        'volumeChanges': coin_info['quotes']['USD']['volume_24h_change_24h'],
        'percentageChanges': str(coin_info['quotes']['USD']['percent_change_24h']),
        'emojiPrice': emoji,
        'emojiPercent': emoji_percent,
        'market_cap': coin_info['quotes']['USD']['market_cap'],
        'rank': coin_info['rank'],
        'ath_price': coin_info['quotes']['USD']['ath_price'],
    }
    return data


def main():
    # get_coin_symbols()
    print(asyncio.run(get_crypto_curr('doge')))
    # print(get_crypto_curr('btc'))
    # print(asyncio.run(get_crypto_curr('btcaesds')))


if __name__ == '__main__':
    main()
