from os.path import splitext
from urllib.parse import urlsplit

import requests


def define_file_extension(url):
    url_path = urlsplit(url).path
    file_path, file_extension = splitext(url_path)
    return file_extension

def download_pictures(url, filepath):
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, 'wb') as file:
        file.write(response.content)