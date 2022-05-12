import os

import requests

from download_pictures import download_pictures


def main():
    path = 'images'
    spacex_api_link = 'https://api.spacexdata.com/v3/launches'
    payload = {'flight_number': '108'}
    response = requests.get(spacex_api_link, params=payload)
    spacex_images = response.json()[0]['links']['flickr_images']
    os.makedirs(path, exist_ok=True)
    for image_number, spacex_image_url in enumerate(spacex_images):
        spacex_photo_filepath = '{}/spacex{}.jpg'.format(path, image_number+1)
        download_pictures(spacex_image_url, spacex_photo_filepath)


if __name__ == '__main__':
    main()
