import os
from datetime import datetime

import pytz
import requests
import json
import shutil
import asyncio

from bs4 import BeautifulSoup


async def get_crypto_fear(current_date, url='https://alternative.me/crypto/fear-and-greed-index/'):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, url)
    soup = BeautifulSoup(response.text, 'html.parser')

    block = soup.find('div', class_='columns').find_all('div', class_='box')
    img_url = block[0].find('img').get('src')
    values = block[1].find_all('div', class_='fng-value')
    new_dict = {}
    for value in values:
        date = value.find(class_='gray').text
        status = value.find(class_='status').text
        num = value.find(class_='fng-circle').text
        new_dict[date] = {
            'status': status,
            'num': num
        }
    with open('./coin_data/templates/fear_index.json', 'w') as file:
        json.dump(new_dict, file, indent=3)
        file.close()

    with open(f'./coin_data/templates/{current_date} fear.png', 'wb') as file:
        shutil.copyfileobj(requests.get(img_url, stream=True).raw, file)
        file.close()

    # with open('../templates/fear_emoji.json', 'w') as file:
    #     emoji = {'Extreme Fear': '🔴', 'Fear': '🟠', 'Neutral': '⚪', 'Greed': '🟡', 'Extreme Greed': '🟢'}
    #     json.dump(emoji, file, indent=3)
    #     file.close()


def main():
    pass
    """ need to change the directory to run this code """
    # files = os.listdir('../templates')
    # tz_london = pytz.timezone('Europe/London')
    # datetime_london = datetime.now(tz_london)
    # current_date = datetime_london.strftime("%Y-%d-%m")
    # img_dates = [img_file for img_file in files if 'fear.png' in img_file]
    # if len(img_dates) == 0:
    #     asyncio.run(get_crypto_fear(current_date=current_date, url='https://alternative.me/crypto/fear-and-greed-index/'))
    #
    # last_date = img_dates[0].split()[0]
    # if last_date != current_date:
    #     asyncio.run(get_crypto_fear(current_date=current_date, url='https://alternative.me/crypto/fear-and-greed-index/'))
    #     os.remove(f"../templates/{last_date} fear.png")
    #     print('fear-coin_data updated')
    # asyncio.run(get_crypto_fear(current_date=current_date, url='https://alternative.me/crypto/fear-and-greed-index/'))


if __name__ == '__main__':
    main()
