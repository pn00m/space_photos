import os


import requests


def get_pictures(url, path, filename):
    try:
        response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.ConnectionError:
        return


def main():
    path = 'images'
    spacex_api_link = 'https://api.spacexdata.com/v3/rockets'
    payload = {'rocket_id': 'falcon_heavy', 'limit': 1, 'offset': 2}
    response = requests.get(spacex_api_link, params=payload)
    spacex_images = response.json()[0]['flickr_images']
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    for image_number, spacex_image_url in enumerate(spacex_images):
        spacex_filename = '{}/spacex{}.jpg'.format(path, image_number + 1)
        get_pictures(spacex_image_url, path, spacex_filename)


if __name__ == '__main__':
    main()
