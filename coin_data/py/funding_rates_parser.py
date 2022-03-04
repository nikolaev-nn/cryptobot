import asyncio
import json

import requests


async def get_funding_rates(ticker):
    rates = await get_coin_data()
    try:
        for rate in rates:
            if ticker == rate['symbol']:
                return {i["exchangeName"]: {"rate": i["rate"], "emoji": "🟢" if i["rate"] >= 0 else "🔴"} for i in rate["uMarginList"]}
    except:
        return KeyError


async def get_coin_data():
    loop = asyncio.get_event_loop()
    request = loop.run_in_executor(None, requests.get, 'https://open-api.coinglass.com/api/fundingRate/v2/home')
    return json.loads((await request).text)['data']


def main():
    # get_coin_symbols()
    print(asyncio.run(get_funding_rates('a')))
    # print(get_crypto_curr('btc'))
    # print(asyncio.run(get_crypto_curr('btcaesds')))


if __name__ == '__main__':
    main()
