import os
import datetime
from os.path import splitext
from urllib.parse import urlsplit

import requests
import telegram
from dotenv import load_dotenv
import time


def file_extension(url):
    split = urlsplit(url).path
    split2 = splitext(split)
    return split2[1]


def get_pictures(url, path, filename):
    try:
        response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.ConnectionError:
        return


def fetch_nasa_epic(path, nasa_api):
    payload = {
        "api_key": f"{nasa_api}",
    }
    for day in range(5):
        input_link = 'https://api.nasa.gov/EPIC/api/natural/date/{}'\
          .format(datetime.date.today()-datetime.timedelta(days=day+2))
        response = requests.get(input_link, params=payload)
        reply = response.json()
        epic_date = datetime.datetime.fromisoformat(reply[0]['date'])
        epic_url = 'https://api.nasa.gov/EPIC/archive/natural/' + \
            '{}/{}/{}/png/{}.png?api_key={}'\
            .format(epic_date.year, epic_date.strftime('%m'),
                    epic_date.strftime('%d'), reply[0]['image'], nasa_api)
        nasa_filename = '{}/nasa_epic{}.png'.format(path, day + 1)
        get_pictures(epic_url, path, nasa_filename)


def fetch_nasa_apod(path, nasa_api):
    input_link = 'https://api.nasa.gov/planetary/apod'
    payload = {"api_key": f"{nasa_api}", "count": 30}
    response = requests.get(input_link, params=payload)
    reply = response.json()
    for image_number, picture in enumerate(reply):
        try:
            nasa_image_url = reply[image_number]['hdurl']
            nasa_filename = '{}/nasa_apod{}{}'.\
                format(path, image_number+1, file_extension(nasa_image_url))
            get_pictures(nasa_image_url, path, nasa_filename)
        except KeyError:
            continue


def fetch_spacex_last_launch(path):
    spacex_api_link = 'https://api.spacexdata.com/v3/rockets'
    payload = {'rocket_id': 'falcon_heavy', 'limit': 1, 'offset': 2}
    response = requests.get(spacex_api_link, params=payload)
    spacex_images = response.json()[0]['flickr_images']
    for image_number, spacex_image_url in enumerate(spacex_images):
        spacex_filename = '{}/spacex{}.jpg'.format(path, image_number + 1)
        get_pictures(spacex_image_url, path, spacex_filename)


def main():
    load_dotenv()
    path = 'images'
    nasa_api = os.environ['NASA_API_KEY']
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    channel_id = os.environ['TELEGRAM_CHANNEL_ID']
    bot = telegram.Bot(token=bot_token)
    while_condition = True
    try:
        cycle_delay = os.environ['DELAY']
    except KeyError:
        cycle_delay = 1
    try:
        os.makedirs(path)
    except FileExistsError:
        print('Папка ' + path + ' уже существует. Удалите её')
        while_condition = False
    while while_condition:
        fetch_spacex_last_launch(path)
        fetch_nasa_apod(path, nasa_api)
        fetch_nasa_epic(path, nasa_api)
        for filenames in os.walk(path):
            for filename in filenames[2]:
                time.sleep(int(cycle_delay))
                bot.send_document(
                                chat_id=channel_id,
                                document=open(path+'/'+filename, 'rb')
                                )
                os.remove(path+'/'+filename)


if __name__ == '__main__':
    main()
