import os

import requests

from download_pictures import *


def fetch_images(spacex_images, path):
    for image_number, spacex_image_url in enumerate(spacex_images):
        file_extension = get_file_extension(spacex_image_url)
        spacex_photo_filepath = '{}/spacex{}{}'\
            .format(path, image_number+1, file_extension)
        download_pictures(spacex_image_url, spacex_photo_filepath)

def main():
    path = 'images'
    spacex_api_link = 'https://api.spacexdata.com/v3/launches'
    launch_value = '108'
    payload = {'flight_number': launch_value}
    response = requests.get(spacex_api_link, params=payload)
    spacex_images = response.json()[0]['links']['flickr_images']
    os.makedirs(path, exist_ok=True)
    fetch_images(spacex_images, path)


if __name__ == '__main__':
    main()
