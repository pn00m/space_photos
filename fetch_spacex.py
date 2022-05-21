import os

import requests

from download_pictures import *


def fetch_images(path):
    spacex_api_link = 'https://api.spacexdata.com/v3/launches'
    launch_value = '108'
    payload = {'flight_number': launch_value}
    response = requests.get(spacex_api_link, params=payload)
    response.raise_for_status
    spacex_images = response.json()[0]['links']['flickr_images']
    for image_number, spacex_image_url in enumerate(spacex_images):
        file_extension = get_file_extension(spacex_image_url)
        spacex_photo_filepath = '{}/spacex{}{}'\
            .format(path, image_number+1, file_extension)
        download_pictures(spacex_image_url, spacex_photo_filepath)

def main():
    path = 'images'
    os.makedirs(path, exist_ok=True)
    fetch_images(path)


if __name__ == '__main__':
    main()
