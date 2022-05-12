import os
import datetime
from os.path import splitext
from urllib.parse import urlsplit


import requests
from dotenv import load_dotenv
from download_pictures import download_pictures


def file_extension(url):
    url_path = urlsplit(url).path
    path_name_extension = splitext(url_path)
    extension = path_name_extension[1]
    return extension


def check_url_accessibility(url, payload):
    try:
        response = requests.get(url, params=payload)
        if (response.status_code in (400, 401, 404)) or\
                ('error' in response):
            return None
    except (
            requests.exceptions.HTTPError,
            requests.exceptions.InvalidURL,
            requests.exceptions.ConnectionError,
    ):
        return None
    return response


def fetch_nasa_epic(path, nasa_api):
    payload = {
        "api_key": {nasa_api},
    }
    epic_photos_amount = 5
    input_link = 'https://api.nasa.gov/EPIC/api/natural'
    epic_base_url = 'https://api.nasa.gov/EPIC/archive/natural/'
    for day in range(epic_photos_amount):
        response = check_url_accessibility(input_link, payload)
        if not response:
            continue
        reply = response.json()
        epic_date = datetime.datetime.fromisoformat(reply[day]['date'])
        epic_url = epic_base_url + '{}/{}/{}/png/{}.png?api_key={}'\
            .format(epic_date.year, epic_date.strftime('%m'),
                    epic_date.strftime('%d'), reply[0]['image'], nasa_api
                    )
        nasa_epic_photo_filepath = '{}/nasa_epic{}.png'.format(path, day + 1)
        download_pictures(epic_url, nasa_epic_photo_filepath)


def fetch_nasa_apod(path, nasa_api):
    input_link = 'https://api.nasa.gov/planetary/apod'
    apod_photos_amount = 30
    payload = {
        "api_key": {nasa_api},
        "count": apod_photos_amount
    }
    response = check_url_accessibility(input_link, payload)
    if not response:
        return
    reply = response.json()
    for image_number, picture in enumerate(reply):
        try:
            nasa_image_url = reply[image_number]['hdurl']
            nasa_apod_filename_extension = file_extension(nasa_image_url)
            nasa_apod_photo_filepath = path + '/nasa_apod' + str(image_number + 1) +\
                nasa_apod_filename_extension
            download_pictures(nasa_image_url, nasa_apod_photo_filepath)
        except KeyError:
            continue


def main():
    load_dotenv()
    path = 'images'
    nasa_api = os.environ['NASA_API_KEY']
    os.makedirs(path, exist_ok=True)
    fetch_nasa_apod(path, nasa_api)
    fetch_nasa_epic(path, nasa_api)


if __name__ == '__main__':
    main()
