import datetime
import os

import requests
from dotenv import load_dotenv

from download_pictures import *


def fetch_nasa_epic_images(path, nasa_api_key):
    payload = {
        "api_key": nasa_api_key,
    }
    epic_photos_amount = 5
    input_link = 'https://api.nasa.gov/EPIC/api/natural'
    epic_base_url = 'https://api.nasa.gov/EPIC/archive/natural/'
    response = requests.get(input_link, params=payload)
    response.raise_for_status
    reply = response.json()
    for day in range(epic_photos_amount):
        epic_date = datetime.datetime.fromisoformat(reply[day]['date'])
        epic_url = '{}{}/png/{}.png?api_key={}'.format(
                        epic_base_url,
                        epic_date.strftime('%Y/%m/%d'),
                        reply[day]['image'],
                        nasa_api_key
                        )
        nasa_epic_photo_filepath = '{}/nasa_epic{}.png'.format(path, day + 1)
        download_pictures(epic_url, nasa_epic_photo_filepath)


def fetch_nasa_apod_images(path, nasa_api_key):
    input_link = 'https://api.nasa.gov/planetary/apod'
    apod_photos_amount = 30
    payload = {
        "api_key": nasa_api_key,
        "count": apod_photos_amount
    }
    response = requests.get(input_link, params=payload)
    reply = response.json()
    for image_number, picture in enumerate(reply):
        try:
            nasa_image_url = reply[image_number]['hdurl']
            apod_filename_extension = get_file_extension(nasa_image_url)
            nasa_apod_photo_filepath = '{}/nasa_apod{}{}'.format(
                path, str(image_number + 1), apod_filename_extension
                )
            download_pictures(nasa_image_url, nasa_apod_photo_filepath)
        except KeyError:
            continue


def main():
    load_dotenv()
    path = 'images'
    nasa_api_key = os.environ['NASA_API_KEY']
    os.makedirs(path, exist_ok=True)
    fetch_nasa_epic_images(path, nasa_api_key)
    fetch_nasa_apod_images(path, nasa_api_key)


if __name__ == '__main__':
    main()
