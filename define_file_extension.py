from os.path import splitext
from urllib.parse import urlsplit


def define_file_extension(url):
    url_path = urlsplit(url).path
    path_name_extension = splitext(url_path)
    file_extension = path_name_extension[1]
    return file_extension