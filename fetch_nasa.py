import os
import datetime
from os.path import splitext
from urllib.parse import urlsplit


import requests
from dotenv import load_dotenv


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


def main():
    load_dotenv()
    path = 'images'
    nasa_api = os.environ['NASA_API_KEY']
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    fetch_nasa_apod(path, nasa_api)
    fetch_nasa_epic(path, nasa_api)


if __name__ == '__main__':
    main()
