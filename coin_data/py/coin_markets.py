import json
import asyncio
import pickle

import requests


async def _save_symbols(tickers, name):
    open_file = open(f'../templates/coin_symbols/{name}.pkl', "wb")
    pickle.dump(tickers, open_file)
    open_file.close()


async def _get_json(url):
    loop = asyncio.get_event_loop()
    request = loop.run_in_executor(None, requests.get, url)
    return json.loads((await request).text)


async def get_coinpaprika(ticker):
    res = await _get_json(f'https://api.coinpaprika.com/v1/tickers/{ticker}')
    return float(res['quotes']['USD']['price'])


async def get_coinex(ticker, sym=False, path='coin_data'):
    ticker = ticker.upper()
    res = (await _get_json('https://api.coinex.com/v1/market/ticker/all'))['data']['ticker']
    if sym is True:
        tickers = [coin.replace('USDT', '') for coin in res if 'USDT' in coin]
        await _save_symbols(tickers, 'CoinEx')
    if ticker in pickle.load(open(f'{path}/templates/coin_symbols/CoinEx.pkl', "rb")):
        return float(res[f'{ticker}USDT']['last'])


async def get_binance(ticker, sym=False, path='coin_data'):
    ticker = ticker.upper()
    res = await _get_json(f'https://api.binance.com/api/v3/ticker/price')
    if sym is True:
        tickers = [coin['symbol'].replace('USDT', '') for coin in res if 'USDT' in coin['symbol']]
        await _save_symbols(tickers, 'Binance')
    if ticker in pickle.load(open(f'{path}/templates/coin_symbols/Binance.pkl', "rb")):
        price = [coin['price'] for coin in res if coin['symbol'] == f'{ticker}USDT'][0]
        return float(price)


async def get_bybit(ticker, sym=False, path='coin_data'):
    ticker = ticker.upper()
    res = await _get_json('https://api-testnet.bybit.com/v2/public/tickers')
    if sym is True:
        tickers = [coin['symbol'].replace('USDT', '') for coin in res['result'] if 'USDT' in coin['symbol']]
        await _save_symbols(tickers, 'ByBit')
    if ticker in pickle.load(open(f'{path}/templates/coin_symbols/ByBit.pkl', "rb")):
        price = [coin['last_price'] for coin in res['result'] if coin['symbol'] == f'{ticker}USDT'][0]
        return float(price)


async def get_kucoin(ticker, sym=False, path='coin_data'):
    ticker = ticker.upper()
    res = await _get_json('https://api.kucoin.com/api/v1/prices')
    if sym is True:
        tickers = [coin for coin in res['data'].keys()]
        await _save_symbols(tickers, 'KuCoin')
    if ticker in pickle.load(open(f'{path}/templates/coin_symbols/KuCoin.pkl', "rb")):
        return float(res['data'][ticker])


async def get_mexc(ticker, sym=False, path='coin_data'):
    ticker = ticker.upper()
    res = await _get_json('https://www.mexc.com/open/api/v2/market/ticker')
    if sym is True:
        tickers = [coin['symbol'].split('_')[0] for coin in res['data'] if 'USDT' in coin['symbol']]
        await _save_symbols(tickers, 'MEXC')
    if ticker in pickle.load(open(f'{path}/templates/coin_symbols/MEXC.pkl', "rb")):
        price = [coin['ask'] for coin in res['data'] if coin['symbol'] == f'{ticker}_USDT'][0]
        return float(price)


async def get_ftx(ticker, sym=False, path='coin_data'):
    ticker = ticker.upper()
    res = await _get_json('https://ftx.com/api/markets')
    if sym is True:
        tickers = [coin['name'].split('/')[0] for coin in res['result'] if '/USDT' in coin['name']]
        await _save_symbols(tickers, 'FTX')
    if ticker in pickle.load(open(f'{path}/templates/coin_symbols/FTX.pkl', "rb")):
        price = [coin['last'] for coin in res['result'] if coin['name'] == f'{ticker}/USDT'][0]
        return float(price)


async def get_gate(ticker, sym=False, path='coin_data'):
    ticker = ticker.upper()
    res = await _get_json('https://data.gateapi.io/api2/1/marketlist')
    if sym is True:
        tickers = [coin['symbol'] for coin in res['data'] if '_usdt' in coin['pair'].lower()]
        await _save_symbols(tickers, 'Gate')
    if ticker in pickle.load(open(f'{path}/templates/coin_symbols/Gate.pkl', "rb")):
        price = [coin['rate'] for coin in res['data'] if coin['pair'] == f'{ticker.lower()}_usdt'][0]
        return float(price)


if __name__ == '__main__':
    t = 'BTC'
    s = False
    p = '..'
    print(asyncio.run(get_coinpaprika('btc-bitcoin')))
    print(asyncio.run(get_coinex(t, s, p)))
    print(asyncio.run(get_binance(t, s, p)))
    print(asyncio.run(get_bybit(t, s, p)))
    print(asyncio.run(get_kucoin(t, s, p)))
    print(asyncio.run(get_mexc(t, s, p)))
    print(asyncio.run(get_ftx(t, s, p)))
    print(asyncio.run(get_gate(t, s, p)))


#
#
    # open_file = open('../templates/coin_symbols/coin_paprika.pkl', "rb")
    # loaded_list = pickle.load(open_file)
    # open_file.close()